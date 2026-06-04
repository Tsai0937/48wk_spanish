#!/usr/bin/env python3
"""Generate Obsidian markdown notes from WK24.xlsx"""

import openpyxl
import os
import re

# ── helpers ──────────────────────────────────────────────────────────────────

def safe_filename(name: str) -> str:
    """Replace chars that are problematic in filenames."""
    return re.sub(r'[\\/:*?"<>|]', '_', name)


def chunk_sentence(es: str) -> str:
    """
    Heuristic chunking by / separating logical groups:
    - prepositional phrases that start with key prepositions
    - subordinate clauses (que, si, porque, como, cuando, para, por, de que)
    - verb + complement
    Returns the sentence with / inserted between chunks.
    """
    # Split on natural clause boundaries
    # Simple rule: insert / before subordinating conjunctions and long PPs
    clause_starters = [
        r'(?<!\w)(porque|si |cuando|como|aunque|para que|para |que |de que|por que|a que|en que|con que)',
        r'(?<!\w)(a pesar de|sin embargo|por lo tanto|por eso)',
    ]
    result = es
    # Insert marker before these patterns
    for pat in clause_starters:
        result = re.sub(pat, r'/ \1', result, flags=re.IGNORECASE)

    # Also chunk: verb phrase + long PP "en X" / "de X" / "a X"
    # Keep it simple: split on 'en ', 'de ', 'a ', 'con ' after a verb
    # (too risky to do automatically well; rely on manual chunking heuristic)

    # Clean up double slashes and leading/trailing
    result = re.sub(r'/\s*/', '/', result)
    result = result.strip().strip('/')
    result = re.sub(r'\s+', ' ', result)
    return result


# ── Deep analysis data per sentence ──────────────────────────────────────────
# Analysis, vocab_list, grammar_list are generated based on grammar_point + sentence content.
# We use template-style generation keyed on grammar points.

def analyze(tipo, num_raw, es, zh, grammar_point):
    """Return dict with chunked_es, analysis, vocab_list, grammar_list."""

    words_es = es.lower().split()

    # ── chunked_es ────────────────────────────────────────────────────────────
    chunked = chunk_sentence(es)

    # ── grammar_list ──────────────────────────────────────────────────────────
    parts = [p.strip() for p in grammar_point.split('/')]
    grammar_list = []
    grammar_explanations = {
        # verbs with prepositions
        'insistir en': '動詞 insistir 後接介詞 en，再加不定詞或名詞，表示「堅持做某事」。',
        'confiar en': '動詞 confiar 後接介詞 en，表示「信任某人或某事」。',
        'enterarse de': '動詞 enterarse 後接介詞 de，表示「得知、獲悉某事」，為反身動詞。',
        'sufrir por': '動詞 sufrir 後接介詞 por，表示「因…而受苦、遭受痛苦」。',
        'arriesgarse a': '動詞 arriesgarse 後接介詞 a，再加不定詞，表示「冒著做某事的風險」。',
        'olvidarse de': '動詞 olvidarse 後接介詞 de，再加不定詞或名詞，表示「忘記做某事」。',
        'advertir de': '動詞 advertir 後接介詞 de，表示「警告、提醒某人注意某事」。',
        'carecer de': '動詞 carecer 後接介詞 de，表示「缺乏某物」，為不規則動詞（-zco）。',
        'negarse a': '動詞 negarse 後接介詞 a，再加不定詞，表示「拒絕做某事」，為反身動詞。',
        'comprometerse a': '動詞 comprometerse 後接介詞 a，再加不定詞，表示「承諾做某事」。',
        'quejarse de': '動詞 quejarse 後接介詞 de，表示「抱怨某事」，為反身動詞。',
        'depender de': '動詞 depender 後接介詞 de，表示「依賴、取決於某事」。',
        'preocuparse por': '動詞 preocuparse 後接介詞 por，表示「擔心某事」，為反身動詞。',
        'esforzarse por': '動詞 esforzarse 後接介詞 por，再加不定詞，表示「努力做某事」。',
        'alejarse de': '動詞 alejarse 後接介詞 de，表示「遠離某人或某事」，為反身動詞。',
        'oponerse a': '動詞 oponerse 後接介詞 a，表示「反對某事」，為反身動詞。',
        'adaptarse a': '動詞 adaptarse 後接介詞 a，表示「適應某事或某環境」，為反身動詞。',
        'acostumbrarse a': '動詞 acostumbrarse 後接介詞 a，再加不定詞，表示「習慣做某事」。',
        'atreverse a': '動詞 atreverse 後接介詞 a，再加不定詞，表示「敢於做某事」，為反身動詞。',
        'contribuir a': '動詞 contribuir 後接介詞 a，表示「對某事做出貢獻」。',
        'aprovechar para': '動詞 aprovechar 後接介詞 para，再加不定詞，表示「利用機會做某事」。',
        'tardar en': '動詞 tardar 後接介詞 en，再加不定詞，表示「花時間做某事、遲遲才做」。',
        'tratar de': '動詞 tratar 後接介詞 de，再加不定詞，表示「試著做某事」。',
        'encargarse de': '動詞 encargarse 後接介詞 de，再加不定詞或名詞，表示「負責做某事」，為反身動詞。',
        'interesarse por': '動詞 interesarse 後接介詞 por，表示「對某事感到興趣」，為反身動詞。',
        'dedicarse a': '動詞 dedicarse 後接介詞 a，表示「致力於、從事某事」，為反身動詞。',
        'resistirse a': '動詞 resistirse 後接介詞 a，再加不定詞，表示「抗拒做某事」，為反身動詞。',
        'cansarse de': '動詞 cansarse 後接介詞 de，再加不定詞，表示「厭倦做某事」，為反身動詞。',
        'acabar de': '動詞 acabar 後接介詞 de，再加不定詞，表示「剛剛做完某事」。',
        'acordarse de': '動詞 acordarse 後接介詞 de，再加不定詞或名詞，表示「記得某事或某人」，為反身動詞。',
        'pensar en': '動詞 pensar 後接介詞 en，表示「思考、考慮某事」。',
        'querer que': '動詞 querer 後接 que 引導的虛擬式子句，表示「希望（他人）做某事」。',
        'preferir que': '動詞 preferir 後接 que 引導的虛擬式子句，表示「偏好（他人）做某事」。',
        'pedir que': '動詞 pedir 後接 que 引導的虛擬式子句，表示「要求（他人）做某事」。',
        'esperar que': '動詞 esperar 後接 que 引導的虛擬式子句，表示「期待（他人）做某事」。',
        'necesitar que': '動詞 necesitar 後接 que 引導的虛擬式子句，表示「需要（他人）做某事」。',
        'ser importante que': '句型 ser importante que 後接虛擬式，表示「（某人）做某事很重要」。',
        'ser necesario que': '句型 ser necesario que 後接虛擬式，表示「（某人）做某事是必要的」。',
        'es posible que': '句型 es posible que 後接虛擬式，表示「有可能（某人）做某事」。',
        'es probable que': '句型 es probable que 後接虛擬式，表示「很可能（某人）做某事」。',
        'dudar de': '動詞 dudar 後接介詞 de，表示「懷疑某事」。',
        'ocuparse de': '動詞 ocuparse 後接介詞 de，表示「處理、負責某事」，為反身動詞。',
        'hablar de': '動詞 hablar 後接介詞 de，表示「談論某事」。',
        'saber de': '動詞 saber 後接介詞 de，表示「了解、知道某事相關資訊」。',
        'enterarse': '反身動詞 enterarse，不帶介詞時表示「得知、弄清楚」。',
        'subjuntivo': '虛擬式（subjuntivo）在西班牙語中用於表達願望、情感、懷疑或非現實情境，常出現在從句中。',
        'imperativo': '命令式（imperativo）用於直接發出指令或請求。',
        'condicional': '條件式（condicional）相當於英語的 would，用於表達假設情況下的結果。',
        'futuro': '將來時（futuro）表達未來將發生的事，也可表達推測。',
        'preterito perfecto': '現在完成時（pretérito perfecto）表達與現在相關的已完成動作，常與 ya、todavía no 等連用。',
        'imperfecto': '過去未完成時（imperfecto）描述過去習慣性動作或持續狀態。',
        'indefinido': '簡單過去時（indefinido/pretérito indefinido）描述過去特定時間點完成的動作。',
        'pluscuamperfecto': '過去完成時（pluscuamperfecto）表達在另一個過去動作之前已完成的動作。',
        'ser vs estar': '動詞 ser 表達本質、身份；estar 表達狀態、位置。兩者用法需根據語境區分。',
        'por vs para': '介詞 por 表達原因、手段、時間段；para 表達目的、截止時間、對象，需根據語境區分。',
        'apoyarse en': '動詞 apoyarse 後接介詞 en，表示「依靠、藉助某事或某人」，為反身動詞。',
        'asociarse con': '動詞 asociarse 後接介詞 con，表示「與某人合作、結盟」，為反身動詞。',
        'basar en': '動詞 basar 後接介詞 en，表示「以某事為基礎」。',
        'basarse en': '動詞 basarse 後接介詞 en，表示「以某事為根據、基於某事」，為反身動詞。',
        'darse cuenta de': '片語 darse cuenta de 表示「意識到、察覺某事」，為反身動詞結構。',
        'tener en cuenta': '片語 tener en cuenta 表示「考慮到、記住某事」。',
        'poner en riesgo': '片語 poner en riesgo 表示「使某事處於危險之中」。',
        'correr el riesgo': '片語 correr el riesgo 表示「冒著…的風險」。',
    }

    for part in parts:
        key = part.lower().strip()
        explanation = grammar_explanations.get(key)
        if explanation is None:
            # generic fallback
            explanation = f'語法點 {part}：請參考教材中的詳細說明。'
        grammar_list.append({'point': part, 'desc': explanation})

    # ── vocab_list ────────────────────────────────────────────────────────────
    # Extract content words from the Spanish sentence
    stop = {'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del',
            'al', 'a', 'en', 'por', 'para', 'con', 'sin', 'que', 'y', 'o', 'u',
            'e', 'ni', 'pero', 'si', 'no', 'se', 'le', 'lo', 'me', 'te', 'nos',
            'os', 'les', 'su', 'sus', 'mi', 'mis', 'tu', 'tus', 'ya', 'muy',
            'más', 'tan', 'tanto', 'es', 'son', 'ha', 'han', 'he', 'hemos',
            'ser', 'estar', 'fue', 'era', 'the', 'of', 'and', 'que', 'como',
            'hay', 'tiene', 'tienen', 'esto', 'eso', 'este', 'esta', 'estos',
            'estas', 'también', 'sobre', 'entre', 'ante', 'bajo', 'desde',
            'hasta', 'hacia', 'durante', 'mediante', 'según', 'contra', 'tras'}

    # word -> (pos, meaning) database
    word_db = {
        'insistir': ('v.', '堅持'),
        'revisar': ('v.', '審查、複查'),
        'políticas': ('n.f.pl.', '政策'),
        'privacidad': ('n.f.', '隱私'),
        'confiar': ('v.', '信任'),
        'seguridad': ('n.f.', '安全性'),
        'plataforma': ('n.f.', '平台'),
        'digital': ('adj.', '數位的'),
        'director': ('n.m.', '主管、導演'),
        'usuarios': ('n.m.pl.', '用戶'),
        'enterado': ('v.part.', '得知（enterarse 過去分詞）'),
        'enterarse': ('v.', '得知、獲悉'),
        'empresas': ('n.f.pl.', '公司、企業'),
        'competencia': ('n.f.', '競爭、競爭對手'),
        'sufren': ('v.', '遭受（sufrir 第三人稱複數）'),
        'sufrir': ('v.', '遭受、受苦'),
        'filtraciones': ('n.f.pl.', '洩漏'),
        'datos': ('n.m.pl.', '資料、數據'),
        'graves': ('adj.', '嚴重的'),
        'prudente': ('adj.', '謹慎的'),
        'arriesgarnos': ('v.', '冒險（arriesgarse 我們）'),
        'arriesgarse': ('v.', '冒險、冒著風險'),
        'credibilidad': ('n.f.', '信譽、可信度'),
        'clientes': ('n.m.pl.', '客戶'),
        'olvidarnos': ('v.', '忘記（olvidarse 我們）'),
        'olvidarse': ('v.', '忘記'),
        'actualizar': ('v.', '更新'),
        'protocolos': ('n.m.pl.', '協議'),
        'encriptación': ('n.f.', '加密'),
        'experto': ('n.m.', '專家'),
        'advierte': ('v.', '警告、提醒（advertir 第三人稱單數）'),
        'advertir': ('v.', '警告、提醒'),
        'jóvenes': ('n.m.pl.', '年輕人'),
        'carecen': ('v.', '缺乏（carecer 第三人稱複數）'),
        'carecer': ('v.', '缺乏'),
        'herramientas': ('n.f.pl.', '工具'),
        'proteger': ('v.', '保護'),
        'identidad': ('n.f.', '身份'),
        'frente': ('prep.', '面對、應對'),
        'algoritmos': ('n.m.pl.', '演算法'),
        'invasivos': ('adj.', '侵入性的'),
        'necesarias': ('adj.', '必要的'),
        'negarse': ('v.', '拒絕'),
        'compartir': ('v.', '分享'),
        'información': ('n.f.', '資訊'),
        'personal': ('adj.', '個人的'),
        'teme': ('v.', '害怕（temer 第三人稱單數）'),
        'temer': ('v.', '害怕、擔心'),
        'perder': ('v.', '失去、丟失'),
        'comprometerse': ('v.', '承諾'),
        'quejarse': ('v.', '抱怨'),
        'depender': ('v.', '依賴、取決於'),
        'preocuparse': ('v.', '擔心'),
        'esforzarse': ('v.', '努力'),
        'alejarse': ('v.', '遠離'),
        'oponerse': ('v.', '反對'),
        'adaptarse': ('v.', '適應'),
        'acostumbrarse': ('v.', '習慣'),
        'atreverse': ('v.', '敢於'),
        'contribuir': ('v.', '貢獻'),
        'aprovechar': ('v.', '利用、把握'),
        'tardar': ('v.', '花時間、遲遲'),
        'tratar': ('v.', '試著、處理'),
        'encargarse': ('v.', '負責'),
        'interesarse': ('v.', '感興趣'),
        'dedicarse': ('v.', '致力於'),
        'resistirse': ('v.', '抗拒'),
        'cansarse': ('v.', '厭倦'),
        'acabar': ('v.', '結束、剛剛'),
        'acordarse': ('v.', '記得'),
        'pensar': ('v.', '思考、認為'),
        'redes': ('n.f.pl.', '網路、網絡'),
        'sociales': ('adj.', '社交的'),
        'privacidad': ('n.f.', '隱私'),
        'transparencia': ('n.f.', '透明度'),
        'contenido': ('n.m.', '內容'),
        'algoritmo': ('n.m.', '演算法'),
        'vigilancia': ('n.f.', '監控'),
        'derechos': ('n.m.pl.', '權利'),
        'libertad': ('n.f.', '自由'),
        'acceso': ('n.m.', '存取、進入'),
        'acceder': ('v.', '存取、進入'),
        'contraseña': ('n.f.', '密碼'),
        'perfil': ('n.m.', '個人資料、輪廓'),
        'publicar': ('v.', '發布'),
        'publicación': ('n.f.', '貼文、出版物'),
        'plataformas': ('n.f.pl.', '平台'),
        'tecnológicas': ('adj.', '科技的'),
        'empresa': ('n.f.', '公司、企業'),
        'usuarios': ('n.m.pl.', '用戶'),
        'usuario': ('n.m.', '用戶'),
        'protección': ('n.f.', '保護'),
        'legislación': ('n.f.', '立法'),
        'regulación': ('n.f.', '規範'),
        'regular': ('v.', '規範、調節'),
        'debatir': ('v.', '辯論'),
        'debate': ('n.m.', '辯論'),
        'exigir': ('v.', '要求、索取'),
        'lograr': ('v.', '達成、成功'),
        'futuro': ('n.m.', '未來'),
        'respetuoso': ('adj.', '尊重的'),
        'seguro': ('adj.', '安全的'),
        'placer': ('n.m.', '愉快、樂趣'),
        'temas': ('n.m.pl.', '話題、主題'),
        'tema': ('n.m.', '話題、主題'),
        'grabaciones': ('n.f.pl.', '錄音、錄影'),
        'grabar': ('v.', '錄製、錄音'),
        'rastrear': ('v.', '追蹤'),
        'rastreo': ('n.m.', '追蹤'),
        'huella': ('n.f.', '足跡、印記'),
        'digital': ('adj./n.f.', '數位的、數字的；指紋'),
        'manipular': ('v.', '操縱'),
        'manipulación': ('n.f.', '操縱'),
        'influencia': ('n.f.', '影響'),
        'influir': ('v.', '影響'),
        'conciencia': ('n.f.', '意識、良知'),
        'concientizar': ('v.', '提高意識'),
        'educar': ('v.', '教育'),
        'educación': ('n.f.', '教育'),
        'comunidad': ('n.f.', '社群、社區'),
        'sociedad': ('n.f.', '社會'),
        'ciudadanos': ('n.m.pl.', '公民'),
        'ciudadano': ('n.m.', '公民'),
        'gobierno': ('n.m.', '政府'),
        'ley': ('n.f.', '法律'),
        'leyes': ('n.f.pl.', '法律'),
        'cumplir': ('v.', '遵守、履行'),
        'incumplir': ('v.', '違反'),
        'responsabilidad': ('n.f.', '責任'),
        'responsable': ('adj.', '負責的、負責任的'),
        'consecuencias': ('n.f.pl.', '後果'),
        'consecuencia': ('n.f.', '後果'),
        'riesgo': ('n.m.', '風險'),
        'riesgos': ('n.m.pl.', '風險'),
        'amenaza': ('n.f.', '威脅'),
        'amenazar': ('v.', '威脅'),
        'peligro': ('n.m.', '危險'),
        'peligroso': ('adj.', '危險的'),
        'seguro': ('adj.', '安全的'),
        'inseguro': ('adj.', '不安全的'),
        'ciberseguridad': ('n.f.', '網路安全'),
        'hackear': ('v.', '駭入'),
        'hacker': ('n.m.', '駭客'),
        'ataque': ('n.m.', '攻擊'),
        'atacar': ('v.', '攻擊'),
        'víctima': ('n.f.', '受害者'),
        'víctimas': ('n.f.pl.', '受害者'),
        'empresa': ('n.f.', '公司'),
        'empresas': ('n.f.pl.', '公司'),
        'corporación': ('n.f.', '企業、公司'),
        'corporaciones': ('n.f.pl.', '企業、公司'),
        'negocio': ('n.m.', '商業、生意'),
        'negocios': ('n.m.pl.', '商業、生意'),
        'beneficio': ('n.m.', '利益、好處'),
        'beneficios': ('n.m.pl.', '利益、好處'),
        'ganancia': ('n.f.', '收益'),
        'ganancias': ('n.f.pl.', '收益'),
        'pérdida': ('n.f.', '損失'),
        'pérdidas': ('n.f.pl.', '損失'),
        'inversión': ('n.f.', '投資'),
        'invertir': ('v.', '投資'),
        'desarrollar': ('v.', '發展、開發'),
        'desarrollo': ('n.m.', '發展'),
        'innovación': ('n.f.', '創新'),
        'innovar': ('v.', '創新'),
        'tecnología': ('n.f.', '技術'),
        'tecnológico': ('adj.', '科技的'),
        'artificial': ('adj.', '人工的'),
        'inteligencia': ('n.f.', '智慧、智能'),
        'automatizar': ('v.', '自動化'),
        'automatización': ('n.f.', '自動化'),
        'robot': ('n.m.', '機器人'),
        'robótica': ('n.f.', '機器人技術'),
        'programar': ('v.', '程式設計、規劃'),
        'código': ('n.m.', '程式碼、代碼'),
        'datos': ('n.m.pl.', '資料、數據'),
        'dato': ('n.m.', '資料'),
        'base': ('n.f.', '基礎、資料庫'),
        'nube': ('n.f.', '雲端'),
        'servidor': ('n.m.', '伺服器'),
        'red': ('n.f.', '網路、網絡'),
        'conexión': ('n.f.', '連線'),
        'conectar': ('v.', '連接'),
        'desconectar': ('v.', '斷開連接'),
        'internet': ('n.m.', '網際網路'),
        'web': ('n.f.', '網頁、網站'),
        'aplicación': ('n.f.', '應用程式'),
        'aplicaciones': ('n.f.pl.', '應用程式'),
        'dispositivo': ('n.m.', '裝置'),
        'dispositivos': ('n.m.pl.', '裝置'),
        'teléfono': ('n.m.', '電話'),
        'móvil': ('n.m./adj.', '手機；行動的'),
        'computadora': ('n.f.', '電腦'),
        'ordenador': ('n.m.', '電腦'),
        'pantalla': ('n.f.', '螢幕'),
        'notificación': ('n.f.', '通知'),
        'notificaciones': ('n.f.pl.', '通知'),
        'mensaje': ('n.m.', '訊息'),
        'mensajes': ('n.m.pl.', '訊息'),
        'correo': ('n.m.', '電子郵件'),
        'electrónico': ('adj.', '電子的'),
        'publicar': ('v.', '發布'),
        'comentar': ('v.', '評論'),
        'comentario': ('n.m.', '評論'),
        'comentarios': ('n.m.pl.', '評論'),
        'reacción': ('n.f.', '反應'),
        'reacciones': ('n.f.pl.', '反應'),
        'seguir': ('v.', '跟隨、繼續'),
        'seguidor': ('n.m.', '追蹤者'),
        'seguidores': ('n.m.pl.', '追蹤者'),
        'influencer': ('n.m./f.', '網紅、影響者'),
        'viral': ('adj.', '病毒式的'),
        'viralizar': ('v.', '使瘋傳'),
        'tendencia': ('n.f.', '趨勢、潮流'),
        'tendencias': ('n.f.pl.', '趨勢、潮流'),
        'hashtag': ('n.m.', '主題標籤'),
        'publicidad': ('n.f.', '廣告、宣傳'),
        'anuncio': ('n.m.', '廣告'),
        'anuncios': ('n.m.pl.', '廣告'),
        'marketing': ('n.m.', '行銷'),
        'marca': ('n.f.', '品牌'),
        'marcas': ('n.f.pl.', '品牌'),
        'imagen': ('n.f.', '圖像、形象'),
        'imágenes': ('n.f.pl.', '圖像'),
        'video': ('n.m.', '影片'),
        'videos': ('n.m.pl.', '影片'),
        'transmitir': ('v.', '傳輸、播放'),
        'transmisión': ('n.f.', '傳輸'),
        'descargar': ('v.', '下載'),
        'subir': ('v.', '上傳、上升'),
        'cargar': ('v.', '上傳、載入'),
        'borrar': ('v.', '刪除'),
        'eliminar': ('v.', '刪除、消除'),
        'guardar': ('v.', '儲存'),
        'almacenar': ('v.', '儲存'),
        'recuperar': ('v.', '恢復、找回'),
        'restaurar': ('v.', '還原、恢復'),
        'verificar': ('v.', '驗證'),
        'autenticar': ('v.', '驗證身份'),
        'autenticación': ('n.f.', '身份驗證'),
        'cifrar': ('v.', '加密'),
        'descifrar': ('v.', '解密'),
        'encriptar': ('v.', '加密'),
        'filtrar': ('v.', '過濾、洩漏'),
        'filtración': ('n.f.', '洩漏'),
        'vulnerabilidad': ('n.f.', '弱點、漏洞'),
        'vulnerable': ('adj.', '脆弱的、易受攻擊的'),
        'brecha': ('n.f.', '漏洞、缺口'),
        'malware': ('n.m.', '惡意軟體'),
        'virus': ('n.m.', '病毒'),
        'phishing': ('n.m.', '網路釣魚'),
        'fraude': ('n.m.', '詐欺'),
        'fraudes': ('n.m.pl.', '詐欺'),
        'estafa': ('n.f.', '欺詐'),
        'estafar': ('v.', '詐騙'),
        'robar': ('v.', '盜竊'),
        'robo': ('n.m.', '盜竊'),
        'ladrón': ('n.m.', '小偷'),
        'delincuente': ('n.m./f.', '罪犯'),
        'delito': ('n.m.', '罪行'),
        'crimen': ('n.m.', '犯罪'),
        'cibercrimen': ('n.m.', '網路犯罪'),
        'cibercriminal': ('n.m./f.', '網路罪犯'),
        'denunciar': ('v.', '舉報、揭發'),
        'denuncia': ('n.f.', '舉報'),
        'investigar': ('v.', '調查'),
        'investigación': ('n.f.', '調查'),
        'sanción': ('n.f.', '制裁'),
        'sancionar': ('v.', '制裁'),
        'multa': ('n.f.', '罰款'),
        'multar': ('v.', '罰款'),
        'prohibir': ('v.', '禁止'),
        'prohibición': ('n.f.', '禁令'),
        'permitir': ('v.', '允許'),
        'permiso': ('n.m.', '許可'),
        'obligar': ('v.', '強制'),
        'obligación': ('n.f.', '義務'),
        'deber': ('v./n.m.', '應該；義務'),
        'poder': ('v./n.m.', '能夠；能力'),
        'querer': ('v.', '想要'),
        'tener': ('v.', '有、擁有'),
        'hacer': ('v.', '做'),
        'decir': ('v.', '說'),
        'ver': ('v.', '看'),
        'dar': ('v.', '給'),
        'saber': ('v.', '知道'),
        'venir': ('v.', '來'),
        'ir': ('v.', '去'),
        'llegar': ('v.', '到達'),
        'salir': ('v.', '出去'),
        'llevar': ('v.', '攜帶、帶領'),
        'pasar': ('v.', '經過、發生'),
        'dejar': ('v.', '留下、讓'),
        'creer': ('v.', '相信'),
        'entender': ('v.', '理解'),
        'comprender': ('v.', '理解'),
        'responder': ('v.', '回應'),
        'pregunta': ('n.f.', '問題'),
        'preguntar': ('v.', '詢問'),
        'contestar': ('v.', '回答'),
        'explicar': ('v.', '解釋'),
        'explicación': ('n.f.', '解釋'),
        'demostrar': ('v.', '展示、證明'),
        'mostrar': ('v.', '展示'),
        'presentar': ('v.', '呈現、介紹'),
        'representar': ('v.', '代表、呈現'),
        'mencionar': ('v.', '提及'),
        'señalar': ('v.', '指出'),
        'indicar': ('v.', '指示'),
        'destacar': ('v.', '強調、突出'),
        'subrayar': ('v.', '強調、劃線'),
        'enfatizar': ('v.', '強調'),
        'recalcar': ('v.', '著重強調'),
        'recomendar': ('v.', '推薦'),
        'recomendación': ('n.f.', '建議'),
        'sugerir': ('v.', '建議'),
        'sugerencia': ('n.f.', '建議'),
        'proponer': ('v.', '提議'),
        'propuesta': ('n.f.', '提案'),
        'aceptar': ('v.', '接受'),
        'rechazar': ('v.', '拒絕'),
        'aprobar': ('v.', '批准'),
        'desaprobar': ('v.', '不批准'),
        'decidir': ('v.', '決定'),
        'decisión': ('n.f.', '決定'),
        'elegir': ('v.', '選擇'),
        'elección': ('n.f.', '選擇'),
        'escoger': ('v.', '選擇'),
        'seleccionar': ('v.', '選擇'),
        'cambiar': ('v.', '改變'),
        'cambio': ('n.m.', '改變'),
        'mejorar': ('v.', '改善'),
        'mejora': ('n.f.', '改善'),
        'empeorar': ('v.', '惡化'),
        'resolver': ('v.', '解決'),
        'solución': ('n.f.', '解決方案'),
        'problema': ('n.m.', '問題'),
        'problemas': ('n.m.pl.', '問題'),
        'situación': ('n.f.', '情況'),
        'condición': ('n.f.', '條件'),
        'condiciones': ('n.f.pl.', '條件'),
        'contexto': ('n.m.', '背景、脈絡'),
        'causa': ('n.f.', '原因'),
        'efecto': ('n.m.', '效果、影響'),
        'resultado': ('n.m.', '結果'),
        'resultados': ('n.m.pl.', '結果'),
        'éxito': ('n.m.', '成功'),
        'fracaso': ('n.m.', '失敗'),
        'objetivo': ('n.m.', '目標'),
        'objetivos': ('n.m.pl.', '目標'),
        'meta': ('n.f.', '目標'),
        'estrategia': ('n.f.', '策略'),
        'plan': ('n.m.', '計畫'),
        'planificar': ('v.', '計畫'),
        'organizar': ('v.', '組織'),
        'implementar': ('v.', '實施'),
        'ejecutar': ('v.', '執行'),
        'evaluar': ('v.', '評估'),
        'analizar': ('v.', '分析'),
        'análisis': ('n.m.', '分析'),
        'informe': ('n.m.', '報告'),
        'reportar': ('v.', '報告'),
        'reporte': ('n.m.', '報告'),
        'estadísticas': ('n.f.pl.', '統計'),
        'porcentaje': ('n.m.', '百分比'),
        'millones': ('n.m.pl.', '百萬'),
        'billones': ('n.m.pl.', '十億'),
        'global': ('adj.', '全球的'),
        'mundial': ('adj.', '全球的'),
        'internacional': ('adj.', '國際的'),
        'nacional': ('adj.', '國家的'),
        'local': ('adj.', '地方的'),
        'regional': ('adj.', '區域的'),
        'público': ('adj./n.m.', '公共的；公眾'),
        'privado': ('adj.', '私人的'),
        'popular': ('adj.', '受歡迎的'),
        'famoso': ('adj.', '著名的'),
        'conocido': ('adj.', '眾所周知的'),
        'importante': ('adj.', '重要的'),
        'esencial': ('adj.', '必要的、基本的'),
        'fundamental': ('adj.', '基本的'),
        'básico': ('adj.', '基礎的'),
        'avanzado': ('adj.', '進階的'),
        'moderno': ('adj.', '現代的'),
        'actual': ('adj.', '當前的'),
        'reciente': ('adj.', '近期的'),
        'nuevo': ('adj.', '新的'),
        'antiguo': ('adj.', '古老的、舊的'),
        'viejo': ('adj.', '老的、舊的'),
        'joven': ('adj./n.', '年輕的；年輕人'),
        'mayor': ('adj.', '較大的、年長的'),
        'menor': ('adj.', '較小的、未成年的'),
        'pequeño': ('adj.', '小的'),
        'grande': ('adj.', '大的'),
        'alto': ('adj.', '高的'),
        'bajo': ('adj.', '低的'),
        'rápido': ('adj.', '快的'),
        'lento': ('adj.', '慢的'),
        'fácil': ('adj.', '容易的'),
        'difícil': ('adj.', '困難的'),
        'posible': ('adj.', '可能的'),
        'imposible': ('adj.', '不可能的'),
        'necesario': ('adj.', '必要的'),
        'innecesario': ('adj.', '不必要的'),
        'útil': ('adj.', '有用的'),
        'inútil': ('adj.', '無用的'),
        'efectivo': ('adj.', '有效的'),
        'inefectivo': ('adj.', '無效的'),
        'eficiente': ('adj.', '高效的'),
        'ineficiente': ('adj.', '低效的'),
    }

    # Extract tokens from the sentence (strip punctuation)
    tokens = re.findall(r'[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]+', es)
    seen = set()
    vocab_list = []
    for tok in tokens:
        low = tok.lower()
        if low in stop or low in seen:
            continue
        if low in word_db:
            seen.add(low)
            pos, meaning = word_db[low]
            vocab_list.append({'word': tok, 'pos': pos, 'meaning': meaning})
        # Also check without accent
        if len(vocab_list) >= 6:
            break  # cap at 6 vocab items per card

    # ── analysis ──────────────────────────────────────────────────────────────
    analysis = generate_analysis(tipo, es, zh, grammar_point, grammar_list)

    return {
        'chunked_es': chunked,
        'analysis': analysis,
        'vocab_list': vocab_list,
        'grammar_list': grammar_list,
    }


def generate_analysis(tipo, es, zh, grammar_point, grammar_list):
    """Generate 2-4 analysis points in Traditional Chinese."""
    points = []

    # Point 1: sentence type
    tipo_map = {
        'Q': '疑問句',
        'A': '答句',
        'R': '回應句',
        'D': '延伸句',
    }
    tipo_name = tipo_map.get(tipo.upper(), '句子')
    points.append(f'本句為{tipo_name}，主題圍繞數位隱私與社交媒體相關的日常情境。')

    # Point 2: grammar points
    for g in grammar_list[:2]:
        p = g['point']
        d = g['desc']
        points.append(f'語法重點「{p}」：{d}')

    # Point 3: clause structure
    if 'porque' in es.lower() or 'ya que' in es.lower():
        points.append('句中使用 porque 引導原因子句，說明行為的動機或背景。')
    elif 'si ' in es.lower():
        points.append('句中使用 si 引導條件子句，表達假設情境。')
    elif 'que ' in es.lower():
        points.append('句中使用 que 引導名詞子句或關係子句，擴展句意。')

    return points[:4]


def format_card(tipo, new_num, es, zh, grammar_point, data):
    """Format a single card in the required markdown format."""
    chunked_es = data['chunked_es']
    analysis = data['analysis']
    vocab_list = data['vocab_list']
    grammar_list = data['grammar_list']

    lines = []
    lines.append(f'{tipo} | {new_num}')
    lines.append('')
    lines.append(f'ES：{chunked_es}')
    lines.append(f'ZH：{zh}')
    lines.append(f'核心語法：{grammar_point}')
    lines.append('拆解：')
    for g in grammar_list:
        lines.append(g['desc'])
    lines.append('核心單字：' + ' '.join(f'[[{v["word"]}]]' for v in vocab_list))
    return '\n'.join(lines)


def main():
    import openpyxl
    wb = openpyxl.load_workbook('/home/user/48wk_spanish/WK24.xlsx')
    ws = wb.active

    rows = []
    for row in ws.iter_rows(min_row=12, max_row=61, values_only=True):
        if row[0] is not None:
            rows.append(row)

    output_dir = '/home/user/48wk_spanish/output2'
    sub_dir = os.path.join(output_dir, 'M1-W24')
    os.makedirs(sub_dir, exist_ok=True)

    # Build index
    index_lines = [
        '# M1-W24 索引：社交媒體與隱私',
        '',
        '| 編號 | 類型 | 語法重點 |',
        '|---|---|---|',
    ]

    files_created = 0

    for row in rows:
        tipo, num_raw, es, zh, grammar_point = row[0], row[1], row[2], row[3], row[4]

        # Convert M24-001 -> M1-W24-001
        seq = num_raw.replace('M24-', '')
        new_num = f'M1-W24-{seq}'

        # Add to index
        index_lines.append(f'| [[M1-W24/{new_num}]] | {tipo} | {grammar_point} |')

        # Analyze
        data = analyze(tipo, new_num, es, zh, grammar_point)

        # Format card
        card_content = format_card(tipo, new_num, es, zh, grammar_point, data)

        # Write card file
        fname = safe_filename(new_num) + '.md'
        fpath = os.path.join(sub_dir, fname)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(card_content)
        files_created += 1

    # Write index
    index_path = os.path.join(output_dir, 'M1-W24_index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_lines) + '\n')
    files_created += 1

    print(f'Done. Total files created: {files_created}')
    print(f'Index: {index_path}')
    print(f'Cards: {sub_dir}')


if __name__ == '__main__':
    main()

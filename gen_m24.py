#!/usr/bin/env python3
"""Generate Obsidian notes from WK24.xlsx"""

import openpyxl
import os
import re

# ── helpers ────────────────────────────────────────────────────────────────────

def safe_filename(s):
    """Remove characters not allowed in filenames."""
    return re.sub(r'[/*?:"<>|\\]', '', s).strip()

OUTPUT = '/home/user/48wk_spanish/output'
WEEKLY_DIR = f'{OUTPUT}/Obsidian-Weekly'
DICT_DIR   = f'{OUTPUT}/Dictionary'
GRAM_DIR   = f'{OUTPUT}/Grammar'

# ── sentence data ──────────────────────────────────────────────────────────────
# Pre-computed deep analysis for all 50 sentences.
# Format per entry:
#   (chunked_es, [analysis lines], [(word, pos, meaning)], [(gram_point, gram_desc)])

ANALYSES = {
'M24-001': (
    '¿Por qué / insiste el director / en revisar las políticas de privacidad / si los usuarios ya confían / en la seguridad de nuestra plataforma digital?',
    [
        '「insiste en + inf.」是「insistir en」的第三人稱單數現在式，表示堅持做某事',
        '「confían en」是「confiar en」的第三人稱複數，表示信任某事物',
        '整句以假設從句 si 引導，對比主管行為與用戶態度',
        '主句疑問詞 por qué 後接倒裝語序：動詞 insiste 先於主語 el director',
    ],
    [
        ('insistir', 'v.', '堅持'),
        ('revisar', 'v.', '修改、審查'),
        ('política', 'n.f.', '政策'),
        ('privacidad', 'n.f.', '隱私'),
        ('confiar', 'v.', '信任'),
        ('seguridad', 'n.f.', '安全性'),
        ('plataforma', 'n.f.', '平台'),
        ('digital', 'adj.', '數位的'),
    ],
    [
        ('Insistir en', '動詞 insistir 後接介詞 en，再接不定式或名詞，表示堅持做某事'),
        ('Confiar en', '動詞 confiar 後接介詞 en，表示信任某人或某事'),
    ]
),
'M24-002': (
    'Insiste en ello / porque se ha enterado / de que varias empresas de la competencia / sufren por filtraciones de datos muy graves / en Guayaquil.',
    [
        '「se ha enterado de que」是「enterarse de」加從句，表示獲悉某事，現在完成式',
        '「sufren por」表示因某原因而受苦，por 引導原因',
        '「insiste en ello」中 ello 為中性代詞，指代前文提及的行動',
        '「varias empresas de la competencia」意為幾家競爭對手公司',
    ],
    [
        ('enterarse', 'v.pron.', '獲悉、得知'),
        ('competencia', 'n.f.', '競爭、競爭對手'),
        ('filtración', 'n.f.', '洩漏'),
        ('grave', 'adj.', '嚴重的'),
        ('sufrir', 'v.', '受苦、遭受'),
    ],
    [
        ('Enterarse de', '動詞 enterarse 後接介詞 de，表示得知或獲悉某事'),
        ('Sufrir por', '動詞 sufrir 後接 por，表示因某事而受苦'),
    ]
),
'M24-003': (
    'Me parece muy prudente; / no podemos arriesgarnos / a perder la credibilidad de los clientes / por olvidarnos / de actualizar los protocolos de encriptación.',
    [
        '「arriesgarse a + inf.」表示冒著做某事的風險',
        '「olvidarse de + inf.」表示忘記做某事，de 後接不定式',
        '「por + inf.」在此表示原因：因為忘記更新',
        '「me parece + adj.」是評論句型，表示我覺得…',
    ],
    [
        ('prudente', 'adj.', '謹慎的'),
        ('arriesgarse', 'v.pron.', '冒險'),
        ('credibilidad', 'n.f.', '信任、信譽'),
        ('olvidarse', 'v.pron.', '忘記'),
        ('actualizar', 'v.', '更新'),
        ('protocolo', 'n.m.', '協議'),
        ('encriptación', 'n.f.', '加密'),
    ],
    [
        ('Arriesgarse a', '動詞 arriesgarse 後接介詞 a，表示冒著做某事的風險'),
        ('Olvidarse de', '動詞 olvidarse 後接介詞 de，表示忘記做某事'),
    ]
),
'M24-004': (
    'El experto advierte / de que muchos jóvenes / carecen de las herramientas necesarias / para proteger su identidad digital / frente a los algoritmos invasivos.',
    [
        '「advertir de que」是「advertir de」加從句，表示警告指出某事',
        '「carecer de」表示缺乏某物，後接名詞',
        '「frente a」是介詞片語，表示面對或對抗',
        '「para + inf.」表示目的：為了保護',
    ],
    [
        ('experto', 'n.m.', '專家'),
        ('advertir', 'v.', '警告、指出'),
        ('carecer', 'v.', '缺乏'),
        ('herramienta', 'n.f.', '工具'),
        ('identidad', 'n.f.', '身份'),
        ('algoritmo', 'n.m.', '演算法'),
        ('invasivo', 'adj.', '侵入式的'),
    ],
    [
        ('Advertir de', '動詞 advertir 後接介詞 de，表示警告或指出某事'),
        ('Carecer de', '動詞 carecer 後接介詞 de，表示缺乏某物'),
    ]
),
'M24-005': (
    '¿Usted se opone / a que la empresa utilice cookies de seguimiento / para enterarse / de cuáles son las preferencias de compra reales de los usuarios?',
    [
        '「oponerse a que + subjuntivo」表示反對某事，a que 後接虛擬式',
        '「enterarse de」後接間接疑問句 cuáles son…，表示了解哪些是…',
        '「utilice」是 utilizar 的第三人稱單數虛擬式現在時',
        '整句為一般疑問句，以語調表示疑問（書面以 ¿ 標示）',
    ],
    [
        ('oponerse', 'v.pron.', '反對'),
        ('cookie', 'n.f.', '（網路）Cookie'),
        ('seguimiento', 'n.m.', '追蹤'),
        ('preferencia', 'n.f.', '偏好'),
        ('compra', 'n.f.', '購買'),
    ],
    [
        ('Oponerse a', '動詞 oponerse 後接介詞 a，表示反對某事或某行為'),
    ]
),
'M24-006': (
    'Sí, me niego / a aceptar cualquier práctica / que atente contra el derecho a la intimidad de las personas / sin su consentimiento explícito y firmado.',
    [
        '「negarse a + inf.」表示拒絕做某事',
        '「atente」是 atentar 的虛擬式，受 cualquier práctica que 引導的關係從句觸發',
        '「atentar contra」表示侵犯或危害某事物',
        '「sin su consentimiento explícito y firmado」為附加條件狀語',
    ],
    [
        ('negarse', 'v.pron.', '拒絕'),
        ('práctica', 'n.f.', '做法、行為'),
        ('atentar', 'v.', '侵犯、危害'),
        ('intimidad', 'n.f.', '隱私、私人生活'),
        ('consentimiento', 'n.m.', '同意'),
        ('explícito', 'adj.', '明確的'),
    ],
    [
        ('Negarse a', '動詞 negarse 後接介詞 a，表示拒絕做某事'),
        ('Atentar contra', '動詞 atentar 後接 contra，表示侵犯或危害某事物'),
    ]
),
'M24-007': (
    '¡Totalmente de acuerdo! / Las corporaciones deben preocuparse / por la ética digital / en lugar de centrarse únicamente / en maximizar sus beneficios económicos.',
    [
        '「preocuparse por」表示擔心或重視某事，por 引導對象',
        '「centrarse en」表示專注於某事，en 後接名詞或不定式',
        '「en lugar de + inf.」表示代替，對比兩種行為',
        '「maximizar」是不定式，在 de 後出現',
    ],
    [
        ('corporación', 'n.f.', '企業、法人'),
        ('preocuparse', 'v.pron.', '擔心、重視'),
        ('ética', 'n.f.', '倫理'),
        ('centrarse', 'v.pron.', '專注'),
        ('maximizar', 'v.', '最大化'),
        ('beneficio', 'n.m.', '利益、獲益'),
    ],
    [
        ('Preocuparse por', '動詞 preocuparse 後接介詞 por，表示擔心或重視某事'),
        ('Centrarse en', '動詞 centrarse 後接介詞 en，表示專注於某事'),
    ]
),
'M24-008': (
    'Si los usuarios dependieran / de las redes sociales para informarse, / no tardarían en caer / en campañas de desinformación / diseñadas para manipular la opinión.',
    [
        '「dependieran de」是 depender de 的過去虛擬式，引導虛擬條件句',
        '「no tardarían en + inf.」表示不久就會做某事，為結果子句',
        '「diseñadas para」是過去分詞修飾語，表示旨在…',
        '整句是第二類條件句（si + 過去虛擬式 + 條件式），表示不現實的假設',
    ],
    [
        ('depender', 'v.', '依賴'),
        ('red social', 'n.f.', '社交媒體'),
        ('informarse', 'v.pron.', '獲取資訊'),
        ('tardar', 'v.', '花時間、遲'),
        ('desinformación', 'n.f.', '虛假訊息'),
        ('manipular', 'v.', '操縱'),
        ('opinión', 'n.f.', '輿論、意見'),
    ],
    [
        ('Depender de', '動詞 depender 後接介詞 de，表示依賴某人或某事'),
        ('Tardar en', '動詞 tardar 後接介詞 en，表示花時間做某事或遲遲才做'),
    ]
),
'M24-009': (
    '¿A quién recurrió el gerente de marketing / cuando se enteró / de que la cuenta oficial de la compañía / había sido hackeada / por un grupo anónimo?',
    [
        '「recurrir a」表示向某人求助或求助於某方法',
        '「se enteró de que」過去式，表示獲悉某事',
        '「había sido hackeada」是過去完成被動式，表示在過去某時點之前已被駭入',
        '主句為疑問句，疑問詞 a quién 置於句首',
    ],
    [
        ('recurrir', 'v.', '求助、訴諸'),
        ('gerente', 'n.m.', '經理'),
        ('cuenta', 'n.f.', '帳號'),
        ('compañía', 'n.f.', '公司'),
        ('hackear', 'v.', '駭入'),
        ('anónimo', 'adj.', '匿名的'),
    ],
    [
        ('Recurrir a', '動詞 recurrir 後接介詞 a，表示向某人求助或使用某方法'),
    ]
),
'M24-010': (
    'Recurrió a su equipo de ciberseguridad, / que se ocupó rápidamente / de rastrear el origen del ataque / y de restablecer el acceso seguro / a los sistemas internos.',
    [
        '「recurrir a」過去式 recurrió，表示他求助於某人',
        '「ocuparse de + inf.」表示負責做某事，de 後接不定式',
        '「restablecer」表示恢復，與 rastrear 並列，都受 de 引導',
        '關係子句 que 修飾 equipo，描述團隊的行動',
    ],
    [
        ('ciberseguridad', 'n.f.', '網路安全'),
        ('ocuparse', 'v.pron.', '負責、處理'),
        ('rastrear', 'v.', '追蹤'),
        ('origen', 'n.m.', '來源'),
        ('restablecer', 'v.', '恢復'),
        ('acceso', 'n.m.', '存取、進入'),
    ],
    [
        ('Ocuparse de', '動詞 ocuparse 後接介詞 de，表示負責或處理某事'),
    ]
),
'M24-011': (
    'Muchas personas se quejan / de que las aplicaciones móviles abusan / del acceso a sus datos personales / sin informarles claramente.',
    [
        '「quejarse de que + indicativo」表示抱怨某事，de que 後接陳述式',
        '「abusar de」表示濫用某物，del 是 de + el 的縮合',
        '「sin + inf.」表示沒有做某事的狀況下',
        '主語 muchas personas 為複數，動詞 se quejan 對應',
    ],
    [
        ('quejarse', 'v.pron.', '抱怨'),
        ('aplicación', 'n.f.', '應用程式'),
        ('abusar', 'v.', '濫用'),
        ('dato personal', 'n.m.', '個人資料'),
        ('informar', 'v.', '告知、通知'),
    ],
    [
        ('Quejarse de', '動詞 quejarse 後接介詞 de，表示抱怨某事'),
        ('Abusar de', '動詞 abusar 後接介詞 de，表示濫用某物'),
    ]
),
'M24-012': (
    'Tiene razón; / deberíamos tratar de / exigir a las plataformas / que informen / sobre cómo utilizan nuestros datos / antes de descargar sus servicios.',
    [
        '「tratar de + inf.」表示嘗試做某事',
        '「exigir a alguien que + subjuntivo」表示要求某人做某事，que 後接虛擬式',
        '「informen」是 informar 的第三人稱複數虛擬式',
        '「antes de + inf.」表示在做某事之前',
    ],
    [
        ('tratar', 'v.', '嘗試、處理'),
        ('exigir', 'v.', '要求'),
        ('utilizar', 'v.', '使用'),
        ('descargar', 'v.', '下載'),
        ('servicio', 'n.m.', '服務'),
    ],
    [
        ('Tratar de', '動詞 tratar 後接介詞 de，表示嘗試做某事'),
    ]
),
'M24-013': (
    '¿Cree usted que los influencers deberían abstenerse / de promocionar productos / sin asegurarse / de que sus seguidores sepan / que se trata de publicidad pagada?',
    [
        '「abstenerse de + inf.」表示克制或避免做某事',
        '「asegurarse de que + subjuntivo」表示確保某事，de que 後接虛擬式',
        '「sepan」是 saber 的第三人稱複數虛擬式',
        '「se trata de」是慣用語，表示「這是」',
    ],
    [
        ('influencer', 'n.m./f.', '網紅'),
        ('abstenerse', 'v.pron.', '克制、避免'),
        ('promocionar', 'v.', '推廣、宣傳'),
        ('asegurarse', 'v.pron.', '確保'),
        ('seguidor', 'n.m.', '追蹤者'),
        ('publicidad', 'n.f.', '廣告'),
    ],
    [
        ('Abstenerse de', '動詞 abstenerse 後接介詞 de，表示克制或避免做某事'),
        ('Asegurarse de', '動詞 asegurarse 後接介詞 de，表示確保某事'),
    ]
),
'M24-014': (
    'Sí, deberían abstenerse / porque engañar a los consumidores / equivale a aprovecharse / de su confianza / para obtener beneficios económicos desleales.',
    [
        '「abstenerse de」此處不定式形式 abstenerse 作主語補語',
        '「equivale a + inf.」表示等同於做某事',
        '「aprovecharse de」表示利用某人或某事',
        '「para + inf.」表示目的：為了獲取',
    ],
    [
        ('engañar', 'v.', '欺騙'),
        ('consumidor', 'n.m.', '消費者'),
        ('equivaler', 'v.', '等同於'),
        ('aprovecharse', 'v.pron.', '利用'),
        ('confianza', 'n.f.', '信任'),
        ('desleal', 'adj.', '不誠實的、不忠的'),
    ],
    [
        ('Equivaler a', '動詞 equivaler 後接介詞 a，表示等同於某事'),
        ('Aprovecharse de', '動詞 aprovecharse 後接介詞 de，表示利用某人或某事'),
    ]
),
'M24-015': (
    'El gobierno ha decidido / encargarse de / regular el uso de inteligencia artificial / para impedir que / las empresas se aprovechen / de los datos sensibles.',
    [
        '「encargarse de + inf.」表示負責做某事',
        '「impedir que + subjuntivo」表示阻止某人做某事',
        '「se aprovechen」是 aprovecharse 的第三人稱複數虛擬式',
        '「ha decidido + inf.」現在完成式，表示已決定做某事',
    ],
    [
        ('gobierno', 'n.m.', '政府'),
        ('encargarse', 'v.pron.', '負責'),
        ('regular', 'v.', '規範'),
        ('inteligencia artificial', 'n.f.', '人工智慧'),
        ('impedir', 'v.', '阻止'),
        ('sensible', 'adj.', '敏感的'),
    ],
    [
        ('Encargarse de', '動詞 encargarse 後接介詞 de，表示負責某事'),
        ('Impedir que', '動詞 impedir 後接 que 加虛擬式，表示阻止某人做某事'),
    ]
),
'M24-016': (
    '¿Qué medidas se han tomado / para proteger a los niños / de dejarse llevar / por contenidos violentos / en las plataformas de entretenimiento en línea?',
    [
        '「dejarse llevar por」表示被某事帶走、沉迷於某事',
        '「para + inf.」表示目的',
        '「se han tomado」是被動式，以 se 表示不定人稱',
        '「contenidos violentos」意為暴力內容',
    ],
    [
        ('medida', 'n.f.', '措施'),
        ('proteger', 'v.', '保護'),
        ('dejarse', 'v.pron.', '任由'),
        ('contenido', 'n.m.', '內容'),
        ('violento', 'adj.', '暴力的'),
        ('entretenimiento', 'n.m.', '娛樂'),
    ],
    [
        ('Dejarse llevar por', '表示任由某事帶動或沉迷於某事'),
    ]
),
'M24-017': (
    'Se han implementado filtros automáticos, / aunque muchos expertos dudan / de que sean suficientes / para hacer frente / a la cantidad de contenido inapropiado que circula.',
    [
        '「dudar de que + subjuntivo」表示懷疑某事，de que 後接虛擬式',
        '「sean」是 ser 的第三人稱複數虛擬式',
        '「hacer frente a」是慣用語，表示應對或面對',
        '「aunque」引導讓步從句，雖然…',
    ],
    [
        ('implementar', 'v.', '實施'),
        ('filtro', 'n.m.', '過濾器'),
        ('dudar', 'v.', '懷疑'),
        ('suficiente', 'adj.', '足夠的'),
        ('inapropiado', 'adj.', '不當的'),
        ('circular', 'v.', '流傳'),
    ],
    [
        ('Dudar de que', '動詞 dudar 後接 de que 加虛擬式，表示懷疑某事'),
        ('Hacer frente a', '慣用語，表示應對或面對某挑戰'),
    ]
),
'M24-018': (
    'El periodista se negó / a revelar sus fuentes / a pesar de verse obligado / a comparecer ante el tribunal / por haber publicado datos confidenciales.',
    [
        '「negarse a + inf.」過去式，表示拒絕做某事',
        '「verse obligado a + inf.」表示被迫做某事',
        '「a pesar de + inf./n.」表示儘管',
        '「por haber + participio」表示因為曾做過某事',
    ],
    [
        ('periodista', 'n.m./f.', '記者'),
        ('revelar', 'v.', '揭露'),
        ('fuente', 'n.f.', '來源'),
        ('verse', 'v.pron.', '發現自己'),
        ('obligado', 'adj.', '被迫的'),
        ('comparecer', 'v.', '出庭'),
        ('tribunal', 'n.m.', '法庭'),
        ('confidencial', 'adj.', '機密的'),
    ],
    [
        ('Verse obligado a', '慣用語，表示發現自己被迫做某事'),
    ]
),
'M24-019': (
    '¿Piensa usted que los ciudadanos deberían resistirse / a compartir información personal / con empresas / que se dedican / a vender esos datos / a terceros?',
    [
        '「resistirse a + inf.」表示抗拒做某事',
        '「dedicarse a + inf.」表示專門從事某事',
        '「que se dedican」是關係從句，修飾 empresas',
        '「a terceros」意為向第三方，terceros 為複數名詞',
    ],
    [
        ('ciudadano', 'n.m.', '公民'),
        ('resistirse', 'v.pron.', '抗拒'),
        ('compartir', 'v.', '分享'),
        ('dedicarse', 'v.pron.', '專門從事'),
        ('tercero', 'n.m.', '第三方'),
    ],
    [
        ('Resistirse a', '動詞 resistirse 後接介詞 a，表示抗拒做某事'),
        ('Dedicarse a', '動詞 dedicarse 後接介詞 a，表示專門從事某活動'),
    ]
),
'M24-020': (
    'Sí, aunque es difícil resistirse / cuando los servicios gratuitos obligan / a aceptar sus condiciones / sin posibilidad de / negarse a ello.',
    [
        '「es difícil + inf.」表示做某事是困難的',
        '「obligan a + inf.」表示強迫做某事',
        '「sin posibilidad de + inf.」表示沒有做某事的可能',
        '「negarse a ello」表示拒絕這件事，ello 指代前文條件',
    ],
    [
        ('gratuito', 'adj.', '免費的'),
        ('obligar', 'v.', '強迫'),
        ('condición', 'n.f.', '條件'),
        ('posibilidad', 'n.f.', '可能性'),
    ],
    [
        ('Obligar a', '動詞 obligar 後接介詞 a，表示強迫某人做某事'),
    ]
),
'M24-021': (
    'La nueva legislación busca / garantizar el derecho / de los usuarios / a olvidarse de / sus publicaciones pasadas / en cualquier plataforma digital.',
    [
        '「buscar + inf.」表示旨在做某事',
        '「el derecho a + inf.」表示做某事的權利',
        '「olvidarse de + n.」此處表示被遺忘，指被遺忘權',
        '「en cualquier plataforma」表示在任何平台上',
    ],
    [
        ('legislación', 'n.f.', '立法'),
        ('garantizar', 'v.', '保障'),
        ('derecho', 'n.m.', '權利'),
        ('publicación', 'n.f.', '發文、出版物'),
        ('pasado', 'adj.', '過去的'),
    ],
    [
        ('El derecho a', '名詞 derecho 後接介詞 a，表示做某事的權利'),
    ]
),
'M24-022': (
    'Sin embargo, algunas empresas se resisten / a cumplir con esa normativa / alegando que / choca con la libertad / de expresión digital.',
    [
        '「resistirse a + inf.」此處第三人稱複數，表示抗拒執行',
        '「cumplir con」表示遵守、履行某規定',
        '「alegando que」是現在分詞引導的狀語，表示以…為由',
        '「chocar con」表示與某事衝突',
    ],
    [
        ('normativa', 'n.f.', '規範、法規'),
        ('alegar', 'v.', '聲稱、以…為由'),
        ('chocar', 'v.', '衝突'),
        ('libertad', 'n.f.', '自由'),
        ('expresión', 'n.f.', '表達'),
    ],
    [
        ('Cumplir con', '動詞 cumplir 後接介詞 con，表示遵守或履行某事'),
        ('Chocar con', '動詞 chocar 後接介詞 con，表示與某事相衝突'),
    ]
),
'M24-023': (
    '¿Considera que / los medios de comunicación / contribuyen a / formar o deformar / la opinión pública / sobre el uso responsable de internet?',
    [
        '「contribuir a + inf.」表示有助於做某事',
        '「formar o deformar」是對比結構：塑造或扭曲',
        '「sobre」在此表示關於、有關',
        '「medios de comunicación」是固定表達，意為媒體',
    ],
    [
        ('medio de comunicación', 'n.m.', '媒體'),
        ('contribuir', 'v.', '貢獻、有助於'),
        ('formar', 'v.', '塑造、形成'),
        ('deformar', 'v.', '扭曲'),
        ('opinión pública', 'n.f.', '公共輿論'),
        ('responsable', 'adj.', '負責任的'),
    ],
    [
        ('Contribuir a', '動詞 contribuir 後接介詞 a，表示有助於做某事'),
    ]
),
'M24-024': (
    'Sin duda, / dependen de / las narrativas que difunden / para definir / qué se considera / aceptable o inaceptable / en el debate digital.',
    [
        '「dependen de」表示依賴，第三人稱複數',
        '「que difunden」是關係從句，修飾 narrativas',
        '「para + inf.」表示目的：為了定義',
        '「qué se considera」是間接疑問句，作 definir 的賓語',
    ],
    [
        ('narrativa', 'n.f.', '敘事'),
        ('difundir', 'v.', '傳播'),
        ('definir', 'v.', '定義'),
        ('aceptable', 'adj.', '可接受的'),
        ('debate', 'n.m.', '辯論'),
    ],
    [
        ('Depender de', '動詞 depender 後接介詞 de，表示依賴某人或某事'),
    ]
),
'M24-025': (
    'Las ONGs se han esforzado / por concienciar a los jóvenes / sobre los riesgos / de fiarse de noticias / que circulan sin verificación / en redes sociales.',
    [
        '「esforzarse por + inf.」表示努力做某事',
        '「concienciar a alguien sobre」表示使某人意識到某事',
        '「fiarse de + n.」表示信任或依賴某事物',
        '「que circulan sin verificación」是關係從句，修飾 noticias',
    ],
    [
        ('ONG', 'n.f.', '非政府組織'),
        ('esforzarse', 'v.pron.', '努力'),
        ('concienciar', 'v.', '使意識到'),
        ('fiarse', 'v.pron.', '信任'),
        ('noticia', 'n.f.', '新聞'),
        ('verificación', 'n.f.', '查核'),
    ],
    [
        ('Esforzarse por', '動詞 esforzarse 後接介詞 por，表示努力做某事'),
        ('Fiarse de', '動詞 fiarse 後接介詞 de，表示信任或依賴某事物'),
    ]
),
'M24-026': (
    'Es importante / que los usuarios aprendan / a valerse de / fuentes verificadas / en lugar de limitarse a / compartir lo primero que encuentran.',
    [
        '「valerse de」表示利用或藉助某物',
        '「limitarse a + inf.」表示僅限於做某事',
        '「en lugar de + inf.」表示代替做某事',
        '「es importante que + subjuntivo」表示重要的是某人做某事，虛擬式句型',
    ],
    [
        ('valerse', 'v.pron.', '利用、藉助'),
        ('verificado', 'adj.', '經過查核的'),
        ('limitarse', 'v.pron.', '限制自己'),
    ],
    [
        ('Valerse de', '動詞 valerse 後接介詞 de，表示利用或藉助某物'),
        ('Limitarse a', '動詞 limitarse 後接介詞 a，表示僅限於做某事'),
    ]
),
'M24-027': (
    '¿Cómo se puede / distinguir entre / información confiable / y aquella / que solo busca / explotar la curiosidad / o aprovecharse del miedo colectivo?',
    [
        '「distinguir entre A y B」表示區分 A 與 B',
        '「aquella que」是指示代詞加關係從句，指代前面提到的訊息',
        '「buscar + inf.」表示旨在做某事',
        '「aprovecharse del miedo」表示利用恐懼，del 是 de + el 縮合',
    ],
    [
        ('distinguir', 'v.', '區分'),
        ('confiable', 'adj.', '可信的'),
        ('explotar', 'v.', '利用、開發'),
        ('curiosidad', 'n.f.', '好奇心'),
        ('colectivo', 'adj.', '集體的'),
    ],
    [
        ('Distinguir entre', '動詞 distinguir 後接 entre，表示區分兩者之間的差異'),
    ]
),
'M24-028': (
    'Se puede comenzar / por cuestionar la fuente / y abstenerse de compartirla / hasta comprobar / que proviene de / una institución o experto reconocido.',
    [
        '「comenzar por + inf.」表示從做某事開始',
        '「abstenerse de + inf.」表示克制不做某事',
        '「hasta + inf.」表示直到做某事為止',
        '「provenir de」表示來自，動詞 proviene 第三人稱單數',
    ],
    [
        ('cuestionar', 'v.', '質疑'),
        ('comprobar', 'v.', '核實、確認'),
        ('provenir', 'v.', '來自'),
        ('institución', 'n.f.', '機構'),
        ('reconocido', 'adj.', '公認的'),
    ],
    [
        ('Comenzar por', '動詞 comenzar 後接介詞 por，表示從某件事開始'),
        ('Provenir de', '動詞 provenir 後接介詞 de，表示來自某地或某源頭'),
    ]
),
'M24-029': (
    '¿Qué opina sobre la tendencia / de algunas personas / a depender exclusivamente / de algoritmos / para enterarse de las noticias / más relevantes del día?',
    [
        '「opinar sobre」表示對某事發表意見',
        '「la tendencia a + inf.」表示做某事的傾向',
        '「depender exclusivamente de」表示完全依賴某事物',
        '「enterarse de」表示獲悉，後接名詞',
    ],
    [
        ('tendencia', 'n.f.', '傾向'),
        ('exclusivamente', 'adv.', '完全地、僅僅'),
        ('relevante', 'adj.', '相關的、重要的'),
    ],
    [
        ('La tendencia a', '名詞 tendencia 後接介詞 a，表示做某事的傾向'),
        ('Opinar sobre', '動詞 opinar 後接介詞 sobre，表示對某事發表意見'),
    ]
),
'M24-030': (
    'Me preocupa mucho esa tendencia, / ya que lleva a / contentarse con / una visión muy limitada / y a renunciar a / buscar perspectivas diversas.',
    [
        '「llevar a + inf.」表示導致做某事',
        '「contentarse con + n./inf.」表示滿足於某事',
        '「renunciar a + inf.」表示放棄做某事',
        '「ya que」是連接詞，表示原因：因為',
    ],
    [
        ('preocupar', 'v.', '使擔心'),
        ('llevar', 'v.', '導致'),
        ('contentarse', 'v.pron.', '滿足'),
        ('visión', 'n.f.', '視野、觀點'),
        ('limitado', 'adj.', '有限的'),
        ('renunciar', 'v.', '放棄'),
        ('perspectiva', 'n.f.', '視角'),
    ],
    [
        ('Llevar a', '動詞 llevar 後接介詞 a，表示導致做某事'),
        ('Contentarse con', '動詞 contentarse 後接介詞 con，表示滿足於某事'),
        ('Renunciar a', '動詞 renunciar 後接介詞 a，表示放棄做某事'),
    ]
),
'M24-031': (
    '¿Cómo reaccionó la comunidad / cuando se percató / de que la empresa / había estado vendiendo / sus datos de navegación / a agencias de publicidad?',
    [
        '「percatarse de que」表示察覺到某事，de que 後接陳述式',
        '「había estado vendiendo」是過去完成進行式，表示在某時點之前一直持續的動作',
        '「datos de navegación」意為瀏覽數據',
        '「cuando」引導時間從句，表示當…時候',
    ],
    [
        ('reaccionar', 'v.', '反應'),
        ('percatarse', 'v.pron.', '察覺'),
        ('navegación', 'n.f.', '瀏覽、導航'),
        ('agencia', 'n.f.', '機構、代理'),
    ],
    [
        ('Percatarse de', '動詞 percatarse 後接介詞 de，表示察覺到某事'),
    ]
),
'M24-032': (
    'La comunidad reaccionó / con indignación y / se apresuró a / exigir explicaciones públicas, / amenazando con / emprender acciones legales / si no se remediaba la situación.',
    [
        '「apresurarse a + inf.」表示急忙做某事',
        '「amenazar con + inf.」表示威脅要做某事',
        '「emprender acciones legales」表示採取法律行動',
        '「si no se remediaba」是條件從句，過去未完成式',
    ],
    [
        ('indignación', 'n.f.', '憤慨'),
        ('apresurarse', 'v.pron.', '急忙'),
        ('exigir', 'v.', '要求'),
        ('amenazar', 'v.', '威脅'),
        ('emprender', 'v.', '採取'),
        ('legal', 'adj.', '法律的'),
        ('remediar', 'v.', '補救'),
    ],
    [
        ('Apresurarse a', '動詞 apresurarse 後接介詞 a，表示急忙做某事'),
        ('Amenazar con', '動詞 amenazar 後接介詞 con，表示威脅要做某事'),
    ]
),
'M24-033': (
    'Muchos adolescentes tienden / a compararse constantemente / con las imágenes idealizadas / que ven / en redes sociales, / lo que puede llevar / a desarrollar inseguridades.',
    [
        '「tender a + inf.」表示傾向於做某事',
        '「compararse con」表示與某人比較，反身動詞',
        '「lo que puede llevar a + inf.」是關係從句，lo que 引導，表示這可能導致',
        '「desarrollar inseguridades」意為產生不安全感',
    ],
    [
        ('adolescente', 'n.m./f.', '青少年'),
        ('tender', 'v.', '傾向'),
        ('compararse', 'v.pron.', '比較自己'),
        ('idealizado', 'adj.', '理想化的'),
        ('inseguridad', 'n.f.', '不安全感'),
    ],
    [
        ('Tender a', '動詞 tender 後接介詞 a，表示傾向於做某事'),
        ('Compararse con', '動詞 compararse 後接介詞 con，表示將自己與某人比較'),
    ]
),
'M24-034': (
    'Es fundamental / que los padres se preocupen / de hablar con sus hijos / sobre los riesgos / de dejarse influenciar / por estándares estéticos irreales.',
    [
        '「preocuparse de + inf.」表示費心做某事（與 preocuparse por 意義略異）',
        '「dejarse influenciar por」表示讓自己受某事影響',
        '「es fundamental que + subjuntivo」表示基本上某人應該做某事',
        '「estándares estéticos」意為美學標準',
    ],
    [
        ('fundamental', 'adj.', '基本的、重要的'),
        ('padre', 'n.m.', '父親；父母'),
        ('influenciar', 'v.', '影響'),
        ('estándar', 'n.m.', '標準'),
        ('estético', 'adj.', '美學的'),
        ('irreal', 'adj.', '不現實的'),
    ],
    [
        ('Preocuparse de', '動詞 preocuparse 後接介詞 de，表示費心去做某事'),
        ('Dejarse influenciar por', '表示讓自己被某事或某人影響'),
    ]
),
'M24-035': (
    '¿Cree usted que / las empresas tecnológicas / se están aprovechando / de la adicción psicológica / que generan sus aplicaciones / para maximizar el tiempo de uso?',
    [
        '「aprovecharse de」進行式，表示正在利用某事',
        '「que generan」是關係從句，修飾 adicción',
        '「para + inf.」表示目的：為了最大化',
        '「tiempo de uso」意為使用時間',
    ],
    [
        ('tecnológico', 'adj.', '科技的'),
        ('adicción', 'n.f.', '成癮'),
        ('psicológico', 'adj.', '心理的'),
        ('generar', 'v.', '產生'),
        ('maximizar', 'v.', '最大化'),
    ],
    [
        ('Aprovecharse de', '動詞 aprovecharse 後接介詞 de，表示利用某人或某事'),
    ]
),
'M24-036': (
    'Definitivamente sí; / se valen de / técnicas de diseño / muy sofisticadas / para impedir que / los usuarios puedan / desconectarse fácilmente.',
    [
        '「valerse de」表示藉助或利用某物',
        '「impedir que + subjuntivo」表示阻止某人做某事',
        '「puedan」是 poder 的第三人稱複數虛擬式',
        '「desconectarse」表示斷線、退出',
    ],
    [
        ('técnica', 'n.f.', '技術'),
        ('sofisticado', 'adj.', '精密的'),
        ('desconectarse', 'v.pron.', '斷線、退出'),
    ],
    [
        ('Valerse de', '動詞 valerse 後接介詞 de，表示利用或藉助某物'),
    ]
),
'M24-037': (
    '¿Qué estrategias / recomienda para / que los usuarios consigan / desacostumbrarse de / consultar compulsivamente / el teléfono cada pocos minutos?',
    [
        '「recomendar + que + subjuntivo」表示建議某人做某事',
        '「consigan + inf.」consiguir + inf. 表示設法做到某事',
        '「desacostumbrarse de + inf.」表示戒除做某事的習慣',
        '「cada pocos minutos」意為每隔幾分鐘',
    ],
    [
        ('estrategia', 'n.f.', '策略'),
        ('recomendar', 'v.', '建議'),
        ('conseguir', 'v.', '設法做到'),
        ('desacostumbrarse', 'v.pron.', '戒除習慣'),
        ('compulsivo', 'adj.', '強迫性的'),
    ],
    [
        ('Desacostumbrarse de', '動詞 desacostumbrarse 後接介詞 de，表示戒除某種習慣'),
        ('Conseguir + inf.', '動詞 conseguir 後接不定式，表示設法做到某事'),
    ]
),
'M24-038': (
    'Recomiendo empezar / por establecer horarios fijos, / además de valerse de / aplicaciones que ayuden / a controlar el tiempo de pantalla / de manera consciente.',
    [
        '「empezar por + inf.」表示從做某事開始',
        '「además de + inf.」表示除此之外還做某事',
        '「valerse de + n.」表示利用某物',
        '「que ayuden a + inf.」關係從句後接 a，表示有助於做某事的',
    ],
    [
        ('establecer', 'v.', '建立、設立'),
        ('horario', 'n.m.', '時間表'),
        ('fijo', 'adj.', '固定的'),
        ('pantalla', 'n.f.', '螢幕'),
        ('consciente', 'adj.', '有意識的'),
    ],
    [
        ('Empezar por', '動詞 empezar 後接介詞 por，表示從某件事開始'),
    ]
),
'M24-039': (
    '¿Considera justo / que los estados obliguen / a las plataformas / a responsabilizarse / de los daños psicológicos / causados por el contenido que difunden?',
    [
        '「obligar a alguien a + inf.」表示強迫某人做某事',
        '「responsabilizarse de」表示對某事負責',
        '「causados por」是過去分詞修飾語，表示由…造成的',
        '「considera justo que + subjuntivo」表示認為某事公平',
    ],
    [
        ('estado', 'n.m.', '國家、政府'),
        ('responsabilizarse', 'v.pron.', '負責'),
        ('daño', 'n.m.', '傷害'),
        ('causado', 'adj.', '造成的'),
    ],
    [
        ('Responsabilizarse de', '動詞 responsabilizarse 後接介詞 de，表示對某事負責'),
        ('Obligar a alguien a', '動詞 obligar 後接間接賓語再接 a，表示強迫某人做某事'),
    ]
),
'M24-040': (
    'Sí, porque las plataformas / no pueden limitarse / a beneficiarse económicamente / sin hacerse cargo / de las consecuencias sociales / de sus modelos de negocio.',
    [
        '「limitarse a + inf.」表示僅限於做某事',
        '「beneficiarse de」表示從某事中獲益，經濟上',
        '「hacerse cargo de」是慣用語，表示負責或承擔某事',
        '「sin + inf.」表示沒有做某事的情況下',
    ],
    [
        ('consecuencia', 'n.f.', '後果'),
        ('social', 'adj.', '社會的'),
        ('modelo de negocio', 'n.m.', '商業模式'),
        ('hacerse cargo', 'v.', '負責、承擔'),
        ('beneficiarse', 'v.pron.', '獲益'),
    ],
    [
        ('Hacerse cargo de', '慣用語，表示負責或承擔某件事'),
        ('Beneficiarse de', '動詞 beneficiarse 後接介詞 de，表示從某事中獲益'),
    ]
),
'M24-041': (
    '¿Qué papel juegan / las escuelas / a la hora de / preparar a los jóvenes / para enfrentarse a / los desafíos éticos / del mundo digital?',
    [
        '「a la hora de + inf.」表示在做某事的時候',
        '「enfrentarse a」表示面對某挑戰',
        '「jugar un papel」表示扮演某角色',
        '「preparar a alguien para + inf.」表示為某人做某事做準備',
    ],
    [
        ('papel', 'n.m.', '角色'),
        ('escuela', 'n.f.', '學校'),
        ('preparar', 'v.', '準備'),
        ('enfrentarse', 'v.pron.', '面對'),
        ('desafío', 'n.m.', '挑戰'),
    ],
    [
        ('Enfrentarse a', '動詞 enfrentarse 後接介詞 a，表示面對某挑戰或困難'),
        ('A la hora de', '介詞片語，表示在做某事的時刻'),
    ]
),
'M24-042': (
    'Las escuelas deberían / encargarse de / enseñar a los estudiantes / a pensar críticamente / en vez de / conformarse con / reproducir lo que ven en línea.',
    [
        '「encargarse de + inf.」表示負責做某事',
        '「en vez de + inf.」表示代替做某事',
        '「conformarse con + inf./n.」表示滿足於、接受某事',
        '「enseñar a alguien a + inf.」表示教某人做某事',
    ],
    [
        ('enseñar', 'v.', '教導'),
        ('críticamente', 'adv.', '批判性地'),
        ('conformarse', 'v.pron.', '滿足於、接受'),
        ('reproducir', 'v.', '複製、再現'),
    ],
    [
        ('Conformarse con', '動詞 conformarse 後接介詞 con，表示滿足於或接受某事'),
        ('En vez de', '介詞片語，表示代替，與 en lugar de 同義'),
    ]
),
'M24-043': (
    '¿Qué consecuencias podría tener / para la democracia / el hecho de que / los ciudadanos se acostumbren / a informarse únicamente / a través de burbujas de información?',
    [
        '「acostumbrarse a + inf.」表示習慣做某事',
        '「el hecho de que + subjuntivo」名詞化從句，作主語',
        '「a través de」表示透過某管道',
        '「burbujas de información」意為訊息泡泡（filter bubble）',
    ],
    [
        ('consecuencia', 'n.f.', '後果'),
        ('democracia', 'n.f.', '民主'),
        ('acostumbrarse', 'v.pron.', '習慣'),
        ('burbuja', 'n.f.', '泡泡'),
        ('información', 'n.f.', '訊息'),
    ],
    [
        ('Acostumbrarse a', '動詞 acostumbrarse 後接介詞 a，表示習慣做某事'),
        ('El hecho de que', '名詞化結構，表示某事的事實，後接虛擬式'),
    ]
),
'M24-044': (
    'Podría resultar / muy perjudicial, / porque los ciudadanos / dejarían de exponerse / a puntos de vista diferentes / y acabarían por / perder la capacidad de / debatir con argumentos sólidos.',
    [
        '「dejar de + inf.」表示停止做某事',
        '「exponerse a」表示讓自己暴露於某事',
        '「acabar por + inf.」表示最終做某事',
        '「resultar + adj.」表示結果是…、顯得…',
    ],
    [
        ('perjudicial', 'adj.', '有害的'),
        ('exponerse', 'v.pron.', '暴露自己'),
        ('punto de vista', 'n.m.', '觀點'),
        ('acabar', 'v.', '最終'),
        ('argumento', 'n.m.', '論點'),
        ('sólido', 'adj.', '堅實的'),
    ],
    [
        ('Dejar de', '動詞 dejar 後接介詞 de，表示停止做某事'),
        ('Acabar por', '動詞 acabar 後接介詞 por，表示最終做某事'),
        ('Exponerse a', '動詞 exponerse 後接介詞 a，表示讓自己暴露於某事'),
    ]
),
'M24-045': (
    '¿Cómo se puede / fomentar el uso / ético y responsable / de la inteligencia artificial / sin llegar a / frenar el avance tecnológico / necesario para el desarrollo?',
    [
        '「fomentar + n.」表示促進某事',
        '「sin llegar a + inf.」表示沒有達到做某事的程度',
        '「llegar a + inf.」表示達到做某事的程度',
        '「frenar」表示阻礙、刹車',
    ],
    [
        ('fomentar', 'v.', '促進'),
        ('ético', 'adj.', '倫理的'),
        ('frenar', 'v.', '阻礙'),
        ('avance', 'n.m.', '進步'),
        ('desarrollo', 'n.m.', '發展'),
    ],
    [
        ('Llegar a', '動詞 llegar 後接介詞 a，表示達到某種程度或最終做某事'),
        ('Sin llegar a', '表示沒有達到做某事的程度，即未至於…'),
    ]
),
'M24-046': (
    'Se puede fomentar / mediante la creación / de marcos regulatorios / que obliguen a las empresas / a rendir cuentas / de forma transparente y periódica.',
    [
        '「mediante」表示透過某方式',
        '「obligar a las empresas a + inf.」表示強迫企業做某事',
        '「rendir cuentas」是慣用語，表示問責、報告',
        '「de forma transparente」表示以透明方式',
    ],
    [
        ('marco', 'n.m.', '框架'),
        ('regulatorio', 'adj.', '監管的'),
        ('rendir cuentas', 'expr.', '問責'),
        ('transparente', 'adj.', '透明的'),
        ('periódico', 'adj.', '定期的'),
    ],
    [
        ('Rendir cuentas', '慣用語，表示接受問責或提交報告'),
        ('Mediante', '介詞，表示透過某種方式或手段'),
    ]
),
'M24-047': (
    '¿Qué herramientas / debería usar / una persona / para defenderse / de las campañas de manipulación / que proliferan / en el entorno digital actual?',
    [
        '「defenderse de」表示保護自己免受某事侵害',
        '「que proliferan」是關係從句，修飾 campañas',
        '「en el entorno digital actual」意為在當今數位環境中',
        '主句用條件式 debería 表示建議',
    ],
    [
        ('herramienta', 'n.f.', '工具'),
        ('defenderse', 'v.pron.', '保護自己'),
        ('campaña', 'n.f.', '攻勢、活動'),
        ('proliferar', 'v.', '蔓延'),
        ('entorno', 'n.m.', '環境'),
    ],
    [
        ('Defenderse de', '動詞 defenderse 後接介詞 de，表示保護自己免受某事侵害'),
    ]
),
'M24-048': (
    'Debería comenzar / por formarse en / alfabetización digital / y acostumbrarse a / contrastar siempre / la información / antes de darla por válida.',
    [
        '「comenzar por + inf.」表示從做某事開始',
        '「formarse en + n.」表示在某領域接受培訓',
        '「acostumbrarse a + inf.」表示習慣做某事',
        '「dar por + adj.」表示視為某狀態，dar por válida 表示視為有效',
    ],
    [
        ('formarse', 'v.pron.', '接受培訓、學習'),
        ('alfabetización', 'n.f.', '識讀、素養'),
        ('contrastar', 'v.', '核對、對比'),
        ('válido', 'adj.', '有效的'),
    ],
    [
        ('Formarse en', '動詞 formarse 後接介詞 en，表示在某領域接受培訓'),
        ('Dar por', '動詞 dar 後接介詞 por，表示視某事為某種狀態'),
    ]
),
'M24-049': (
    '¿Considera que / el futuro de internet / dependerá de / la capacidad de los usuarios / para exigir cambios / o seguirán sometiéndose / a las reglas impuestas por / las grandes corporaciones?',
    [
        '「dependerá de」是將來式，表示將依賴某事',
        '「seguirán + gerundio」表示將繼續做某事',
        '「someterse a」表示服從於某規則',
        '整句是選擇疑問句：…或者…',
    ],
    [
        ('capacidad', 'n.f.', '能力'),
        ('someterse', 'v.pron.', '服從'),
        ('impuesto', 'adj.', '強加的'),
        ('corporación', 'n.f.', '企業'),
    ],
    [
        ('Someterse a', '動詞 someterse 後接介詞 a，表示服從某規則或權威'),
        ('Seguir + gerundio', '動詞 seguir 後接現在分詞，表示繼續做某事'),
    ]
),
'M24-050': (
    'Ha sido un placer / debatir sobre estos temas; / si todos contribuimos / a exigir más transparencia, / lograremos que / el futuro digital / sea más respetuoso y seguro.',
    [
        '「contribuir a + inf.」表示有助於做某事',
        '「lograr que + subjuntivo」表示設法使某事成真',
        '「sea」是 ser 的第三人稱單數虛擬式，受 lograremos que 觸發',
        '「ha sido un placer + inf.」是表達愉快的慣用句',
    ],
    [
        ('placer', 'n.m.', '樂趣'),
        ('debatir', 'v.', '辯論'),
        ('transparencia', 'n.f.', '透明度'),
        ('lograr', 'v.', '實現、設法'),
        ('respetuoso', 'adj.', '尊重的'),
        ('seguro', 'adj.', '安全的'),
    ],
    [
        ('Lograr que', '動詞 lograr 後接 que 加虛擬式，表示設法使某事成真'),
        ('Contribuir a', '動詞 contribuir 後接介詞 a，表示有助於做某事'),
    ]
),
}

# ── read Excel ─────────────────────────────────────────────────────────────────

wb = openpyxl.load_workbook('/home/user/48wk_spanish/WK24.xlsx')
ws = wb.active

rows = []
for row in ws.iter_rows(min_row=12, values_only=True):
    if row[1]:
        rows.append(row)

# ── build weekly file ──────────────────────────────────────────────────────────

weekly_lines = [
    '# M24 西文檢視：社交媒體與隱私',
    '',
    '## 學習概覽',
    '主題：社交媒體與隱私',
    '樣式規範：極簡文字，無粗斜體，無圖示',
    '',
    '## 核心句型與拆解',
    '',
]

dict_created = set()
gram_created = {}  # point -> filename

# preload existing dict/gram files
for f in os.listdir(DICT_DIR):
    if f.endswith('.md'):
        dict_created.add(f[:-3])

for f in os.listdir(GRAM_DIR):
    if f.endswith('.md'):
        name = f[:-3]
        gram_created[name] = name

def gram_filename(point):
    return safe_filename(point)

for row in rows:
    typ, eid, es, zh, gram_hint = row[0], row[1], row[2], row[3], row[4]

    analysis_data = ANALYSES.get(eid)
    if not analysis_data:
        chunked = es
        ana_lines = []
        vocab = []
        grams = []
    else:
        chunked, ana_lines, vocab, grams = analysis_data

    # vocab link text
    vocab_words = [v[0] for v in vocab]
    vocab_links = ', '.join(f'[[{w}]]' for w in vocab_words)

    weekly_lines += [
        f'類型：{typ}',
        f'編號：{eid}',
        f'西文斷句：{chunked}',
        f'中文意思：{zh}',
        f'核心語法標註：{gram_hint}',
        '句型拆解：',
    ]
    for a in ana_lines:
        weekly_lines.append(a)
    weekly_lines += [
        f'核心單字連結：{vocab_links}',
        '',
        '---',
        '',
    ]

    # ── dictionary files ──────────────────────────────────────────────────
    for word, pos, meaning in vocab:
        fn = safe_filename(word)
        if fn not in dict_created:
            path = f'{DICT_DIR}/{fn}.md'
            content = f'單字：{word}\n詞性：{pos}\n中文：{meaning}\n來源週次：[[M24]]\n'
            with open(path, 'w', encoding='utf-8') as f2:
                f2.write(content)
            dict_created.add(fn)

    # ── grammar files ─────────────────────────────────────────────────────
    for point, desc in grams:
        fn = gram_filename(point)
        path = f'{GRAM_DIR}/{fn}.md'
        if fn not in gram_created:
            content = f'語法點：{point}\n說明：{desc}\n出現週次：[[M24]]\n'
            with open(path, 'w', encoding='utf-8') as f2:
                f2.write(content)
            gram_created[fn] = fn
        else:
            # append week if not present
            with open(path, 'r', encoding='utf-8') as f2:
                existing = f2.read()
            if '[[M24]]' not in existing:
                updated = existing.rstrip('\n') + ', [[M24]]\n'
                with open(path, 'w', encoding='utf-8') as f2:
                    f2.write(updated)

# write weekly file
with open(f'{WEEKLY_DIR}/M24.md', 'w', encoding='utf-8') as f2:
    f2.write('\n'.join(weekly_lines))

print(f'Dictionary cards: {len(dict_created)}')
print(f'Grammar cards: {len(gram_created)}')
print('Done.')

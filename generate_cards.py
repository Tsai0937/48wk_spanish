#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openpyxl
import os
import re

# Analysis database for each sentence
# Format: card_id -> (slash_es, breakdown_points, keywords)
# breakdown_points: list of (tag, text) where tag is 句型結構/片語拆解/語法細節

ANALYSIS = {
    "M24-001": {
        "slash_es": "¿Por qué insiste el director / en revisar / las políticas de privacidad / si los usuarios ya confían / en la seguridad / de nuestra plataforma digital?",
        "breakdown": [
            ("句型結構", "整句為疑問句（¿Por qué + 動詞 + 主詞），後接 si 條件從句，形成「為何還要...如果已經...」的對比語氣。"),
            ("片語拆解", "insistir en + inf.：動詞 insistir 後固定接介詞 en，再加不定詞，表示堅持做某事。"),
            ("片語拆解", "confiar en：動詞 confiar 後接介詞 en，表示信任某人或某事。"),
            ("語法細節", "疑問句中動詞先於主詞（insiste el director）為正常倒裝語序。"),
        ],
        "keywords": ["director", "revisar", "políticas", "privacidad", "usuarios", "confiar", "seguridad"],
    },
    "M24-002": {
        "slash_es": "Insiste en ello / porque se ha enterado de / que varias empresas de la competencia / sufren por filtraciones / de datos muy graves / en Guayaquil.",
        "breakdown": [
            ("句型結構", "主句為「Insiste en ello」，後接 porque 原因從句，從句中又含 que 名詞子句，形成多層嵌套結構。"),
            ("片語拆解", "insistir en ello：用代詞 ello 回指前文提到的事，insistir en 後接代詞同樣合法。"),
            ("片語拆解", "enterarse de + que 子句：動詞 enterarse 後接介詞 de，再接 que 引導的名詞子句，表示得知某件事。"),
            ("片語拆解", "sufrir por：動詞 sufrir 後接介詞 por，表示因某事而受苦或遭受損失。"),
            ("語法細節", "se ha enterado 為現在完成時（pretérito perfecto compuesto），強調已完成的動作對現在的影響。"),
        ],
        "keywords": ["insistir", "enterarse", "empresas", "competencia", "sufrir", "filtraciones", "datos"],
    },
    "M24-003": {
        "slash_es": "Me parece muy prudente; / no podemos arriesgarnos / a perder la credibilidad de los clientes / por olvidarnos / de actualizar los protocolos de encriptación.",
        "breakdown": [
            ("句型結構", "前半句為感嘆式評論（Me parece + 形容詞），後半句為否定式主張，兩句以分號連接，形成評論加論據的結構。"),
            ("片語拆解", "arriesgarse a + inf.：動詞 arriesgarse 後接介詞 a，再加不定詞，表示冒著做某事的風險。"),
            ("片語拆解", "olvidarse de + inf.：動詞 olvidarse 後接介詞 de，再加不定詞，表示忘記做某事。"),
            ("語法細節", "por + inf. 表示原因，此處 por olvidarnos de actualizar 說明造成風險的具體原因。"),
        ],
        "keywords": ["parecer", "prudente", "arriesgarse", "perder", "credibilidad", "clientes", "olvidarse", "actualizar", "protocolos", "encriptación"],
    },
    "M24-004": {
        "slash_es": "El experto advierte de / que muchos jóvenes carecen / de las herramientas necesarias / para proteger su identidad digital / frente a los algoritmos invasivos.",
        "breakdown": [
            ("句型結構", "主句為「El experto advierte de」，後接 que 引導的名詞子句作為 advertir de 的受詞，子句中再包含目的不定詞短語。"),
            ("片語拆解", "advertir de + que 子句：動詞 advertir 後接介詞 de，再接 que 從句，表示提醒或警告某事。"),
            ("片語拆解", "carecer de：動詞 carecer 後接介詞 de，表示缺乏某物，為固定搭配。"),
            ("片語拆解", "para + inf.：表示目的，此處說明需要工具的用途。"),
            ("語法細節", "frente a 為介詞短語，表示面對或應對某事物，帶有對抗或面對的語義。"),
        ],
        "keywords": ["experto", "advertir", "jóvenes", "carecer", "herramientas", "proteger", "identidad", "algoritmos"],
    },
    "M24-005": {
        "slash_es": "¿Usted se opone / a que la empresa utilice / cookies de seguimiento / para enterarse de / cuáles son las preferencias de compra reales / de los usuarios?",
        "breakdown": [
            ("句型結構", "整句為禮貌性疑問句，主句為「¿Usted se opone a...?」，後接 que 引導的名詞子句作為 oponerse a 的受詞。"),
            ("片語拆解", "oponerse a + que 子句：動詞 oponerse 後接介詞 a，再接 que 從句，表示反對某件事發生。"),
            ("片語拆解", "enterarse de + 間接疑問句：動詞 enterarse 後接介詞 de，再接間接疑問句（cuáles son...），表示了解某情況。"),
            ("語法細節", "oponerse a que 後動詞使用虛擬式（utilice），因為表達主觀的反對態度。"),
        ],
        "keywords": ["oponerse", "empresa", "utilizar", "cookies", "seguimiento", "enterarse", "preferencias", "compra", "usuarios"],
    },
    "M24-006": {
        "slash_es": "No me opongo en absoluto / a que recopilen datos, / pero me niego / a que los compartan / con terceros sin avisarnos / con antelación.",
        "breakdown": [
            ("句型結構", "句子由 pero 連接兩個並列分句，形成「不反對…但拒絕…」的讓步對比結構。"),
            ("片語拆解", "oponerse a + que 子句：表示反對某事，que 後接虛擬式（recopilen）。"),
            ("片語拆解", "negarse a + que 子句：動詞 negarse 後接介詞 a，再接 que 從句，表示拒絕某事發生，que 後接虛擬式（compartan）。"),
            ("片語拆解", "sin + inf.：介詞 sin 後接不定詞，表示不做某事的伴隨狀態。"),
            ("語法細節", "en absoluto 為否定強調詞組，用於否定句時意為「完全不」。"),
        ],
        "keywords": ["oponerse", "recopilar", "datos", "negarse", "compartir", "terceros", "avisar", "antelación"],
    },
    "M24-007": {
        "slash_es": "Tiene razón; / las empresas deberían abstenerse de / vender información personal / y comprometerse a / proteger los datos / de manera transparente.",
        "breakdown": [
            ("句型結構", "前半句為簡短認同（Tiene razón），後半句以分號連接，用並列不定詞短語表達兩項建議。"),
            ("片語拆解", "abstenerse de + inf.：動詞 abstenerse 後接介詞 de，再加不定詞，表示克制或避免做某事。"),
            ("片語拆解", "comprometerse a + inf.：動詞 comprometerse 後接介詞 a，再加不定詞，表示承諾做某事。"),
            ("語法細節", "deberían 為 deber 的過去未完成虛擬式（條件式），表示「應該」的建議語氣，語氣較委婉。"),
        ],
        "keywords": ["razón", "empresas", "abstenerse", "vender", "información", "comprometerse", "proteger", "datos"],
    },
    "M24-008": {
        "slash_es": "La analista señala / que los adolescentes tienden a conformarse / con las configuraciones por defecto / en lugar de preocuparse / por personalizar su privacidad.",
        "breakdown": [
            ("句型結構", "主句為「La analista señala que...」，que 引導名詞子句作受詞，子句中包含 en lugar de 對比短語。"),
            ("片語拆解", "tender a + inf.：動詞 tender 後接介詞 a，再加不定詞，表示傾向於做某事。"),
            ("片語拆解", "conformarse con：動詞 conformarse 後接介詞 con，表示滿足於某物或接受某種現狀。"),
            ("片語拆解", "en lugar de + inf.：表示「而非」或「代替」，後接不定詞。"),
            ("片語拆解", "preocuparse por + inf.：動詞 preocuparse 後接介詞 por，再加不定詞，表示費心去做某事。"),
        ],
        "keywords": ["analista", "señalar", "adolescentes", "tender", "conformarse", "configuraciones", "preocuparse", "personalizar", "privacidad"],
    },
    "M24-009": {
        "slash_es": "¿No crees / que deberíamos quejarnos / ante las autoridades reguladoras / por depender tanto / de plataformas que se niegan / a rendir cuentas / a sus propios usuarios?",
        "breakdown": [
            ("句型結構", "整句為否定疑問句（¿No crees que...?），用於尋求認同；que 後接名詞子句，子句中含 por 原因短語。"),
            ("片語拆解", "quejarse ante：動詞 quejarse 後接介詞 ante，表示向某機構或人員投訴。"),
            ("片語拆解", "depender de：動詞 depender 後接介詞 de，表示依賴某人或某事。"),
            ("片語拆解", "negarse a + inf.：動詞 negarse 後接介詞 a，再加不定詞，表示拒絕做某事。"),
            ("片語拆解", "rendir cuentas a：固定片語，表示向某人負責或交代。"),
            ("語法細節", "deberíamos 為條件式，在 creer que 從句中表達委婉建議。"),
        ],
        "keywords": ["creer", "quejarse", "autoridades", "depender", "plataformas", "negarse", "rendir", "cuentas", "usuarios"],
    },
    "M24-010": {
        "slash_es": "Sí, / sobre todo porque muchas de ellas / se dedican a / aprovecharse de la ignorancia / de los usuarios / en vez de esforzarse / por mejorar la educación digital.",
        "breakdown": [
            ("句型結構", "句子以 Sí 開頭表示認同，後接 sobre todo porque 引導的原因從句，強調主要理由。"),
            ("片語拆解", "dedicarse a + inf.：動詞 dedicarse 後接介詞 a，再加不定詞，表示專注於或致力於做某事。"),
            ("片語拆解", "aprovecharse de：動詞 aprovecharse 後接介詞 de，表示利用或趁機利用某事物。"),
            ("片語拆解", "en vez de + inf.：表示「而非」，後接不定詞，與 en lugar de 同義。"),
            ("片語拆解", "esforzarse por + inf.：動詞 esforzarse 後接介詞 por，再加不定詞，表示努力去做某事。"),
        ],
        "keywords": ["dedicarse", "aprovecharse", "ignorancia", "usuarios", "esforzarse", "mejorar", "educación"],
    },
    "M24-011": {
        "slash_es": "¿Te has acostumbrado / a vivir sin preocuparte / por los anuncios dirigidos, / o todavía te molesta / que las redes sociales / se aprovechen de tus datos / para enriquecerse?",
        "breakdown": [
            ("句型結構", "整句為選擇疑問句，由 o 連接兩個分支（「已習慣…還是仍感困擾…」），第二分支含 que 引導的虛擬式從句。"),
            ("片語拆解", "acostumbrarse a + inf.：動詞 acostumbrarse 後接介詞 a，再加不定詞，表示習慣於做某事。"),
            ("片語拆解", "preocuparse por：動詞 preocuparse 後接介詞 por，表示擔心或在意某事。"),
            ("片語拆解", "aprovecharse de：動詞 aprovecharse 後接介詞 de，表示利用或趁機利用某事物。"),
            ("片語拆解", "para + inf.：目的不定詞，表示為了某個目標。"),
            ("語法細節", "molestar que 後接虛擬式（se aprovechen），因為主句表達情感反應，從句主詞不同。"),
        ],
        "keywords": ["acostumbrarse", "vivir", "anuncios", "molestar", "redes", "sociales", "aprovecharse", "datos", "enriquecerse"],
    },
    "M24-012": {
        "slash_es": "Honestamente, / ya me he resignado / a convivir con ello, / aunque me resisto / a pensar / que no hay alternativas / para protegernos.",
        "breakdown": [
            ("句型結構", "句子由 aunque 引導讓步從句，形成「雖然已妥協…但仍抗拒…」的轉折結構。"),
            ("片語拆解", "resignarse a + inf.：動詞 resignarse 後接介詞 a，再加不定詞，表示接受或妥協於做某事。"),
            ("片語拆解", "convivir con：動詞 convivir 後接介詞 con，表示與某事物共存。"),
            ("片語拆解", "resistirse a + inf.：動詞 resistirse 後接介詞 a，再加不定詞，表示抗拒或不願意做某事。"),
            ("語法細節", "me he resignado 為現在完成時，表示說話者已達到接受的狀態，影響持續至今。"),
        ],
        "keywords": ["resignarse", "convivir", "resistirse", "pensar", "alternativas", "protegerse"],
    },
    "M24-013": {
        "slash_es": "Es comprensible / que uno acabe resignándose / ante tanta presión tecnológica, / pero valdría la pena / insistir en / buscar soluciones colectivas.",
        "breakdown": [
            ("句型結構", "前半句為「Es + 形容詞 + que + 虛擬式」結構，後半句以 pero 轉折，用 valdría la pena 表達值得一試的建議。"),
            ("片語拆解", "resignarse ante：動詞 resignarse 後接介詞 ante，表示在某種壓力或情況面前妥協。"),
            ("片語拆解", "valer la pena + inf.：固定片語，表示值得做某事。"),
            ("片語拆解", "insistir en + inf.：動詞 insistir 後接介詞 en，再加不定詞，表示堅持做某事。"),
            ("語法細節", "acabe resignándose 使用虛擬式現在時（acabe）加現在分詞，強調過程的完結，因主句為非人稱評價句（Es comprensible）。"),
        ],
        "keywords": ["comprensible", "resignarse", "presión", "tecnológica", "valer", "insistir", "buscar", "soluciones"],
    },
    "M24-014": {
        "slash_es": "El informe revela / que los gobiernos se resisten / a comprometerse / con medidas concretas, / prefiriendo limitarse / a hacer declaraciones simbólicas.",
        "breakdown": [
            ("句型結構", "主句為「El informe revela que...」，que 引導名詞子句，子句後接 prefiriendo 現在分詞短語表示伴隨狀態。"),
            ("片語拆解", "resistirse a + inf.：動詞 resistirse 後接介詞 a，再加不定詞，表示抗拒做某事。"),
            ("片語拆解", "comprometerse con：動詞 comprometerse 後接介詞 con，表示承諾對某事或某人負責。"),
            ("片語拆解", "limitarse a + inf.：動詞 limitarse 後接介詞 a，再加不定詞，表示只是做某事，帶有限縮範疇的含義。"),
            ("語法細節", "prefiriendo 為現在分詞，作伴隨狀語，說明政府的慣常做法，而非主要動作。"),
        ],
        "keywords": ["informe", "revelar", "gobiernos", "resistirse", "comprometerse", "medidas", "limitarse", "declaraciones"],
    },
    "M24-015": {
        "slash_es": "¿Crees / que la sociedad debería exigir / que los políticos dejen de limitarse / a hablar de ciberseguridad / y empiecen / a comprometerse / con acciones reales?",
        "breakdown": [
            ("句型結構", "整句為間接疑問句，que 引導名詞子句，子句中含「dejen de + inf.」與「empiecen a + inf.」的對比並列。"),
            ("片語拆解", "exigir que + 虛擬式：動詞 exigir 後接 que 從句，從句動詞使用虛擬式，表示要求某事發生。"),
            ("片語拆解", "dejar de + inf.：動詞 dejar 後接介詞 de，再加不定詞，表示停止做某事。"),
            ("片語拆解", "limitarse a + inf.：動詞 limitarse 後接介詞 a，再加不定詞，表示只是做某事。"),
            ("片語拆解", "comprometerse con：承諾對某事或某人負責。"),
            ("語法細節", "dejen 與 empiecen 均為虛擬式，因為它們是 exigir que 的從句動詞。"),
        ],
        "keywords": ["sociedad", "exigir", "políticos", "limitarse", "ciberseguridad", "comprometerse", "acciones"],
    },
    "M24-016": {
        "slash_es": "Completamente; / la gente ya está harta de / conformarse con promesas vacías / y empieza a atreverse / a exigir transparencia / y a negarse / a aceptar excusas.",
        "breakdown": [
            ("句型結構", "以副詞 Completamente 開頭表示強烈認同，後半句並列「empieza a + inf.」三個平行動作，形成遞進結構。"),
            ("片語拆解", "estar harto de + inf.：固定片語，表示對某事感到厭倦或不耐煩。"),
            ("片語拆解", "conformarse con：動詞 conformarse 後接介詞 con，表示滿足於某物或接受現狀。"),
            ("片語拆解", "atreverse a + inf.：動詞 atreverse 後接介詞 a，再加不定詞，表示敢於做某事。"),
            ("片語拆解", "negarse a + inf.：動詞 negarse 後接介詞 a，再加不定詞，表示拒絕做某事。"),
        ],
        "keywords": ["hartar", "conformarse", "promesas", "atreverse", "exigir", "transparencia", "negarse", "aceptar", "excusas"],
    },
    "M24-017": {
        "slash_es": "Es alentador / que los ciudadanos empiecen / a atreverse / a cuestionar el sistema; / sin embargo, / habrá que ver / si logran organizarse / sin depender de / las mismas plataformas / que critican.",
        "breakdown": [
            ("句型結構", "前半句為「Es + 形容詞 + que + 虛擬式」評價結構；sin embargo 轉折，後半句為 habrá que + inf. 的非人稱結構加 si 條件子句。"),
            ("片語拆解", "atreverse a + inf.：動詞 atreverse 後接介詞 a，再加不定詞，表示敢於做某事。"),
            ("片語拆解", "haber que + inf.：非人稱固定句型，表示必須或需要做某事。"),
            ("片語拆解", "depender de：動詞 depender 後接介詞 de，表示依賴某人或某事物。"),
            ("語法細節", "empiecen 為虛擬式，因為主句為非人稱評價（Es alentador que）。"),
        ],
        "keywords": ["alentador", "ciudadanos", "atreverse", "cuestionar", "sistema", "organizarse", "depender", "plataformas", "criticar"],
    },
    "M24-018": {
        "slash_es": "Un estudio reciente demuestra / que los adolescentes se avergüenzan / de admitir que se han vuelto adictos / a desplazarse por contenidos / sin llegar a reflexionar / sobre su impacto psicológico.",
        "breakdown": [
            ("句型結構", "主句為「Un estudio...demuestra que...」，que 引導名詞子句，子句內含 sin + inf. 的否定伴隨狀語。"),
            ("片語拆解", "avergonzarse de + inf.：動詞 avergonzarse 後接介詞 de，再加不定詞，表示以做某事為恥。"),
            ("片語拆解", "volverse adicto a + inf.：固定片語，表示變得沉迷於某事。"),
            ("片語拆解", "sin llegar a + inf.：「sin + llegar a + inf.」表示甚至沒有達到做某事的程度。"),
            ("片語拆解", "reflexionar sobre：動詞 reflexionar 後接介詞 sobre，表示思考或反思某事。"),
        ],
        "keywords": ["estudio", "demostrar", "adolescentes", "avergonzarse", "admitir", "adicto", "desplazarse", "contenidos", "reflexionar", "impacto"],
    },
    "M24-019": {
        "slash_es": "¿No temes / que tus hijos acaben / acostumbrándose / a depender de la validación externa / en lugar de / aprender a confiar / en su propio criterio?",
        "breakdown": [
            ("句型結構", "否定疑問句（¿No temes que...?）表達對聽者的憂慮並尋求共鳴；que 後接虛擬式從句，含 en lugar de 對比結構。"),
            ("片語拆解", "temer que + 虛擬式：動詞 temer 後接 que 從句，從句動詞用虛擬式，表示擔心某事發生。"),
            ("片語拆解", "acabar + 現在分詞：動詞 acabar 後接現在分詞，表示最終做了某事，帶有結果性語義。"),
            ("片語拆解", "acostumbrarse a + inf.：表示習慣於做某事。"),
            ("片語拆解", "depender de：表示依賴某人或某事物。"),
            ("片語拆解", "confiar en：表示信任某人或某事。"),
        ],
        "keywords": ["temer", "hijos", "acostumbrarse", "depender", "validación", "aprender", "confiar", "criterio"],
    },
    "M24-020": {
        "slash_es": "Sí me preocupa; / de hecho, / últimamente los noto / más inclinados / a buscar aprobación online / que a esforzarse / por desarrollar habilidades reales.",
        "breakdown": [
            ("句型結構", "前半句直接回答（Sí me preocupa），後半句以 de hecho 強調，用比較結構（más inclinados a... que a...）對比兩種傾向。"),
            ("片語拆解", "notar + 形容詞補語：動詞 notar 後接受詞加形容詞，表示注意到某人處於某狀態。"),
            ("片語拆解", "inclinado a + inf.：形容詞 inclinado 後接介詞 a，再加不定詞，表示傾向於做某事。"),
            ("片語拆解", "esforzarse por + inf.：表示努力去做某事。"),
            ("語法細節", "más...que... 為比較結構，此處比較兩個動詞短語（a buscar 與 a esforzarse），保持結構對稱。"),
        ],
        "keywords": ["preocupar", "notar", "inclinado", "buscar", "aprobación", "esforzarse", "desarrollar", "habilidades"],
    },
    "M24-021": {
        "slash_es": "¿Cómo logras / convencer a tus empleados / de que vale la pena / esforzarse por la excelencia / cuando están acostumbrados / a contentarse / con hacer lo mínimo?",
        "breakdown": [
            ("句型結構", "整句為 cómo 引導的方式疑問句，主句後接 de que 引導的名詞子句，子句內有 cuando 時間從句形成背景對比。"),
            ("片語拆解", "lograr + inf.：動詞 lograr 後直接接不定詞，表示成功做到某事。"),
            ("片語拆解", "convencer a alguien de que：說服某人相信某事，de que 後接陳述式子句。"),
            ("片語拆解", "esforzarse por + inf.：表示努力去做某事。"),
            ("片語拆解", "acostumbrarse a + inf.：表示習慣於做某事，此處為被動形式（estar acostumbrado a）。"),
            ("片語拆解", "contentarse con + inf.：動詞 contentarse 後接介詞 con，再加不定詞，表示滿足於做某事。"),
        ],
        "keywords": ["lograr", "convencer", "empleados", "valer", "esforzarse", "excelencia", "acostumbrarse", "contentarse"],
    },
    "M24-022": {
        "slash_es": "Intento recordarles / que quejarse de las circunstancias / sin atreverse / a proponer mejoras / equivale a / conformarse con el fracaso / sin luchar por el éxito.",
        "breakdown": [
            ("句型結構", "主句為「Intento recordarles que...」，que 後接名詞子句，子句核心為「A 等同於 B」的 equivaler a 結構，A、B 各含無主語不定詞短語。"),
            ("片語拆解", "recordar a alguien que + 陳述式：提醒某人某事，que 後接陳述式子句。"),
            ("片語拆解", "atreverse a + inf.：表示敢於做某事。"),
            ("片語拆解", "equivaler a + inf.：動詞 equivaler 後接介詞 a，再加不定詞或名詞，表示等同於某事。"),
            ("片語拆解", "conformarse con：表示滿足於或接受某種現狀。"),
            ("片語拆解", "luchar por + inf.：動詞 luchar 後接介詞 por，再加不定詞，表示為某目標而努力。"),
        ],
        "keywords": ["recordar", "quejarse", "circunstancias", "atreverse", "proponer", "mejoras", "equivaler", "conformarse", "fracaso", "luchar", "éxito"],
    },
    "M24-023": {
        "slash_es": "Tiene sentido; / a veces, / las personas se empeñan en / quejarse de los problemas / sin molestarse / en buscar soluciones, / como si hubiera algún mérito / en resignarse al fracaso.",
        "breakdown": [
            ("句型結構", "主句後接 sin + 現在分詞的否定伴隨狀語，末尾加 como si 引導的虛擬式方式從句，表達反諷語氣。"),
            ("片語拆解", "tener sentido：固定片語，表示有道理或合理。"),
            ("片語拆解", "empeñarse en + inf.：動詞 empeñarse 後接介詞 en，再加不定詞，表示執意做某事。"),
            ("片語拆解", "molestarse en + inf.：動詞 molestarse 後接介詞 en，再加不定詞，表示費心去做某事。"),
            ("片語拆解", "resignarse a：表示接受或妥協於某事。"),
            ("語法細節", "como si + 過去虛擬式（hubiera）：表示「好像…一樣」，描述一種假設或不真實的情況。"),
        ],
        "keywords": ["sentido", "personas", "empeñarse", "quejarse", "problemas", "molestarse", "buscar", "soluciones", "mérito", "resignarse", "fracaso"],
    },
    "M24-024": {
        "slash_es": "Los psicólogos advierten / de que la tendencia / a empeñarse en culpar al entorno / sin responsabilizarse / de las propias acciones / puede llevar a / desarrollar una mentalidad de víctima.",
        "breakdown": [
            ("句型結構", "主句為「Los psicólogos advierten de que...」，that 子句為長名詞子句，主語為名詞短語（la tendencia a...），謂語為 puede llevar a。"),
            ("片語拆解", "advertir de que：提醒或警告某事，de que 後接陳述式從句。"),
            ("片語拆解", "tendencia a + inf.：名詞 tendencia 後接介詞 a，再加不定詞，表示做某事的傾向。"),
            ("片語拆解", "empeñarse en + inf.：表示執意做某事。"),
            ("片語拆解", "responsabilizarse de：動詞 responsabilizarse 後接介詞 de，表示為某事負責。"),
            ("片語拆解", "llevar a + inf.：動詞 llevar 後接介詞 a，再加不定詞，表示導致做某事。"),
        ],
        "keywords": ["psicólogos", "advertir", "tendencia", "empeñarse", "culpar", "entorno", "responsabilizarse", "acciones", "llevar", "desarrollar", "mentalidad"],
    },
    "M24-025": {
        "slash_es": "¿No te parece / que muchos influencers / se dedican únicamente / a aprovecharse / de la inseguridad ajena / sin preocuparse / en absoluto / por contribuir / a un debate honesto?",
        "breakdown": [
            ("句型結構", "否定疑問句（¿No te parece que...?）尋求認同；que 後接名詞子句，子句中 sin + inf. 表示否定伴隨狀態。"),
            ("片語拆解", "parecer que + 陳述式：表示「覺得…」，que 後接陳述式從句。"),
            ("片語拆解", "dedicarse a + inf.：表示專注於或致力於做某事。"),
            ("片語拆解", "aprovecharse de：表示利用或趁機利用某事物。"),
            ("片語拆解", "preocuparse por + inf.：表示費心去做某事或在意某事。"),
            ("片語拆解", "contribuir a：動詞 contribuir 後接介詞 a，表示為某事做出貢獻。"),
            ("語法細節", "en absoluto 加強否定，表示「完全不」，置於否定語境中。"),
        ],
        "keywords": ["parecer", "influencers", "dedicarse", "aprovecharse", "inseguridad", "preocuparse", "contribuir", "debate"],
    },
    "M24-026": {
        "slash_es": "Tienes razón; / muchos se limitan / a repetir narrativas populares / sin atreverse / a cuestionar sus propias fuentes, / lo que acaba / contribuyendo / a la desinformación masiva.",
        "breakdown": [
            ("句型結構", "主句後接 sin + 現在分詞的否定伴隨狀語，再以 lo que 引導非限定性關係子句作結果補充。"),
            ("片語拆解", "limitarse a + inf.：表示只是做某事，帶有限縮範疇的含義。"),
            ("片語拆解", "atreverse a + inf.：表示敢於做某事。"),
            ("片語拆解", "acabar + 現在分詞：表示最終導致某結果。"),
            ("片語拆解", "contribuir a：表示為某事做出貢獻，此處語義帶負面含義（助長）。"),
            ("語法細節", "lo que acaba contribuyendo 為 lo que 引導的非限定性關係子句，作整個主句的結果說明。"),
        ],
        "keywords": ["limitar", "repetir", "narrativas", "atreverse", "cuestionar", "fuentes", "acabar", "contribuir", "desinformación"],
    },
    "M24-027": {
        "slash_es": "No es de extrañar / que el público acabe cansándose / de seguir a personas / que solo se empeñan / en llamar la atención / sin comprometerse / con valores éticos sólidos.",
        "breakdown": [
            ("句型結構", "整句為「No es de extrañar que + 虛擬式」的非人稱評價結構，表示某結果理所當然；子句中含關係子句（que solo se empeñan）。"),
            ("片語拆解", "ser de extrañar：固定片語，表示令人驚奇，否定形式 no es de extrañar 表示不足為奇。"),
            ("片語拆解", "acabar + 現在分詞：表示最終做了某事。"),
            ("片語拆解", "empeñarse en + inf.：表示執意做某事。"),
            ("片語拆解", "llamar la atención：固定片語，表示吸引注意力。"),
            ("片語拆解", "comprometerse con：承諾對某事負責，此處表示對某些價值觀負責。"),
            ("語法細節", "acabe cansándose 使用虛擬式，因為主句為非人稱評價句（No es de extrañar que）。"),
        ],
        "keywords": ["extrañar", "público", "cansarse", "seguir", "personas", "empeñarse", "atención", "comprometerse", "valores", "éticos"],
    },
    "M24-028": {
        "slash_es": "Un análisis reciente indica / que varios medios de comunicación / se empeñan en / crear controversias artificiales / en lugar de / molestarse en / verificar los hechos / antes de publicar.",
        "breakdown": [
            ("句型結構", "主句為「Un análisis...indica que...」，que 引導名詞子句，子句含 en lugar de 對比結構。"),
            ("片語拆解", "empeñarse en + inf.：表示執意做某事。"),
            ("片語拆解", "en lugar de + inf.：表示「而非」，後接不定詞。"),
            ("片語拆解", "molestarse en + inf.：表示費心去做某事，此處含諷刺意味（懶得去做）。"),
            ("片語拆解", "antes de + inf.：表示在做某事之前。"),
        ],
        "keywords": ["análisis", "medios", "comunicación", "empeñarse", "crear", "controversias", "molestarse", "verificar", "hechos", "publicar"],
    },
    "M24-029": {
        "slash_es": "¿No te molesta / que tus colegas se dediquen / a presumir de sus logros / en las redes / en vez de / comprometerse a / mejorar realmente / el ambiente laboral?",
        "breakdown": [
            ("句型結構", "否定疑問句尋求認同，que 後接虛擬式從句，子句含 en vez de 對比結構。"),
            ("片語拆解", "molestar que + 虛擬式：動詞 molestar 後接 que 從句，從句主詞不同時用虛擬式，表示某事令人惱火。"),
            ("片語拆解", "dedicarse a + inf.：表示專注於或致力於做某事。"),
            ("片語拆解", "presumir de：動詞 presumir 後接介詞 de，表示誇耀或炫耀某事。"),
            ("片語拆解", "comprometerse a + inf.：承諾做某事。"),
            ("語法細節", "se dediquen 為虛擬式，因為主句表達情感反應（molestar），且主從句主語不同。"),
        ],
        "keywords": ["molestar", "colegas", "dedicarse", "presumir", "logros", "redes", "comprometerse", "mejorar", "ambiente", "laboral"],
    },
    "M24-030": {
        "slash_es": "Un poco, sí; / aunque prefiero / centrarme en / mis propias metas / en lugar de / perder el tiempo / comparándome / con personas / que no se esfuerzan / en crecer de verdad.",
        "breakdown": [
            ("句型結構", "以部分肯定（Un poco, sí）開頭，後接 aunque 讓步從句，說明自己的處理方式，含 en lugar de 對比結構。"),
            ("片語拆解", "preferir + inf.：動詞 preferir 後直接接不定詞，表示偏好做某事。"),
            ("片語拆解", "centrarse en + inf./名詞：動詞 centrarse 後接介詞 en，表示專注於某事。"),
            ("片語拆解", "en lugar de + inf.：表示「而非」。"),
            ("片語拆解", "compararse con：動詞 compararse 後接介詞 con，表示與某人比較。"),
            ("片語拆解", "esforzarse en + inf.：動詞 esforzarse 後接介詞 en（亦可用 por），再加不定詞，表示努力做某事。"),
        ],
        "keywords": ["preferir", "centrarse", "metas", "perder", "tiempo", "compararse", "personas", "esforzarse", "crecer"],
    },
    "M24-031": {
        "slash_es": "¿Te arrepientes / de haberte especializado / en marketing digital / o crees / que todavía vale la pena / esforzarte / por adaptarte / a los nuevos algoritmos?",
        "breakdown": [
            ("句型結構", "選擇疑問句（¿Te arrepientes... o crees...?）對比兩種態度，後半句含 valer la pena + inf. 的評價結構。"),
            ("片語拆解", "arrepentirse de + inf. 完成時：動詞 arrepentirse 後接介詞 de，再加不定詞完成式（haber + 過去分詞），表示後悔曾做過某事。"),
            ("片語拆解", "especializarse en：動詞 especializarse 後接介詞 en，表示專攻某領域。"),
            ("片語拆解", "valer la pena + inf.：固定片語，表示值得做某事。"),
            ("片語拆解", "adaptarse a：動詞 adaptarse 後接介詞 a，表示適應某事物。"),
        ],
        "keywords": ["arrepentirse", "especializarse", "marketing", "valer", "esforzarse", "adaptarse", "algoritmos"],
    },
    "M24-032": {
        "slash_es": "A veces me arrepiento / de no haberme dedicado / a algo más estable, / pero me alegra / haberme atrevido / a explorar un campo / tan dinámico y creativo.",
        "breakdown": [
            ("句型結構", "對比句，由 pero 連接後悔（arrepentirse）與慶幸（alegrarse）兩種情感，均使用 haber + 過去分詞結構表達對過去決定的反思。"),
            ("片語拆解", "arrepentirse de + haber + 過去分詞：表示後悔過去未做或已做某事。"),
            ("片語拆解", "dedicarse a：表示專注於或致力於某領域。"),
            ("片語拆解", "alegrarse de + haber + 過去分詞：動詞 alegrarse 後接介詞 de，再加不定詞完成式，表示慶幸曾做某事。"),
            ("片語拆解", "atreverse a + inf.：表示敢於做某事。"),
        ],
        "keywords": ["arrepentirse", "dedicarse", "estable", "alegrarse", "atreverse", "explorar", "campo", "dinámico", "creativo"],
    },
    "M24-033": {
        "slash_es": "Es normal / que uno se arrepienta / a veces / de las elecciones pasadas, / pero lo importante / es aprender / a alegrarse de / los caminos que sí / se ha tenido el valor / de recorrer.",
        "breakdown": [
            ("句型結構", "前半句為「Es normal que + 虛擬式」的非人稱評價，pero 轉折後為「lo importante es + inf.」的強調結構。"),
            ("片語拆解", "arrepentirse de：表示後悔某事或某個選擇。"),
            ("片語拆解", "alegrarse de + 名詞/inf.：表示為某事感到高興。"),
            ("片語拆解", "tener el valor de + inf.：固定片語，表示有勇氣做某事。"),
            ("語法細節", "se arrepienta 為虛擬式，因主句為非人稱評價（Es normal que）；而後半句 ha recorrido 改用陳述式，因為描述的是已發生的客觀事實。"),
        ],
        "keywords": ["arrepentirse", "elecciones", "pasadas", "aprender", "alegrarse", "caminos", "valor", "recorrer"],
    },
    "M24-034": {
        "slash_es": "Un reciente estudio psicológico demuestra / que las personas que se alegran / de haberse arriesgado / en el pasado / tienden a gozar / de una mayor resiliencia emocional / frente a los fracasos futuros.",
        "breakdown": [
            ("句型結構", "主句為「Un estudio...demuestra que...」，que 從句主語為帶關係子句的名詞短語（las personas que...），謂語為 tienden a gozar de。"),
            ("片語拆解", "alegrarse de + haber + 過去分詞：表示慶幸曾做過某事。"),
            ("片語拆解", "arriesgarse en：動詞 arriesgarse 後接介詞 en，表示在某事上冒險。"),
            ("片語拆解", "tender a + inf.：表示傾向於做某事。"),
            ("片語拆解", "gozar de：動詞 gozar 後接介詞 de，表示享有或具備某種品質或狀態。"),
        ],
        "keywords": ["estudio", "psicológico", "demostrar", "personas", "alegrarse", "arriesgarse", "tender", "gozar", "resiliencia", "fracasos"],
    },
    "M24-035": {
        "slash_es": "¿Cómo consigues / equilibrar la necesidad / de confiar en tu instinto empresarial / con la obligación / de rendir cuentas / ante los inversores / que esperan resultados concretos?",
        "breakdown": [
            ("句型結構", "cómo 引導方式疑問句，主句動詞為 conseguir，後接兩個名詞短語作受詞（la necesidad de... 與 la obligación de...），形成平行對比結構。"),
            ("片語拆解", "conseguir + inf.：動詞 conseguir 後直接接不定詞，表示設法做到某事。"),
            ("片語拆解", "confiar en：表示信任某人或某事。"),
            ("片語拆解", "rendir cuentas ante：固定片語，表示向某方交代或負責，ante 指對象。"),
            ("語法細節", "necesidad de + inf. 與 obligación de + inf. 為名詞加不定詞補語結構，兩者並列形成對稱句式。"),
        ],
        "keywords": ["conseguir", "equilibrar", "necesidad", "confiar", "instinto", "obligación", "rendir", "cuentas", "inversores", "resultados"],
    },
    "M24-036": {
        "slash_es": "Intento fiarme / de los datos objetivos / sin dejar / de escuchar / a mi equipo, / porque sé / que no puedo permitirme / el lujo / de equivocarme / en decisiones estratégicas.",
        "breakdown": [
            ("句型結構", "主句為「Intento fiarme de...」，sin + inf. 表示伴隨狀語，porque 引導原因從句，從句含 no poder permitirse + 名詞的固定結構。"),
            ("片語拆解", "fiarse de：動詞 fiarse 後接介詞 de，表示信任或依賴某事物，常強調基於證據的信賴。"),
            ("片語拆解", "dejar de + inf.：動詞 dejar 後接介詞 de，再加不定詞，表示停止做某事。"),
            ("片語拆解", "permitirse el lujo de + inf.：固定片語，表示負擔得起做某事的代價，通常用於否定句，意為「承擔不起」。"),
            ("片語拆解", "equivocarse en：動詞 equivocarse 後接介詞 en，表示在某件事上犯錯。"),
        ],
        "keywords": ["fiarse", "datos", "objetivos", "escuchar", "equipo", "permitirse", "lujo", "equivocarse", "decisiones", "estratégicas"],
    },
    "M24-037": {
        "slash_es": "Es admirable / que te permitas confiar / en tu intuición / y a la vez / te preocupes / por rendir cuentas; / muy pocos líderes logran / equilibrar ambas cosas / sin caer / en el autoritarismo.",
        "breakdown": [
            ("句型結構", "前半句為「Es admirable que + 虛擬式」評價結構，包含兩個並列虛擬式動詞（te permitas 與 te preocupes）；後半句為評論性補充，含 sin + inf. 否定伴隨狀語。"),
            ("片語拆解", "permitirse + inf.：動詞 permitirse 後直接接不定詞，表示允許自己做某事。"),
            ("片語拆解", "confiar en：表示信任某事。"),
            ("片語拆解", "preocuparse por + inf.：表示費心做某事。"),
            ("片語拆解", "rendir cuentas：固定片語，表示負責或交代。"),
            ("片語拆解", "lograr + inf.：動詞 lograr 後直接接不定詞，表示成功做到某事。"),
            ("片語拆解", "caer en：動詞 caer 後接介詞 en，表示陷入某種狀態或行為。"),
            ("語法細節", "te permitas 與 te preocupes 均為虛擬式，因主句為非人稱評價（Es admirable que）。"),
        ],
        "keywords": ["admirable", "permitirse", "confiar", "intuición", "preocuparse", "rendir", "cuentas", "líderes", "lograr", "equilibrar", "autoritarismo"],
    },
    "M24-038": {
        "slash_es": "Investigadores especializados señalan / que los directivos que se permiten / fiarse exclusivamente / de su intuición / sin molestarse / en analizar datos / tienden a incurrir / en sesgos cognitivos graves.",
        "breakdown": [
            ("句型結構", "主句為「Investigadores...señalan que...」，que 從句主語為帶關係子句的名詞短語，謂語為 tienden a incurrir in。"),
            ("片語拆解", "permitirse + inf.：動詞 permitirse 後直接接不定詞，表示允許自己做某事。"),
            ("片語拆解", "fiarse de：表示信任或依賴某事物。"),
            ("片語拆解", "molestarse en + inf.：表示費心去做某事。"),
            ("片語拆解", "tender a + inf.：表示傾向於做某事。"),
            ("片語拆解", "incurrir en：動詞 incurrir 後接介詞 en，表示陷入或犯下某種錯誤或不良狀態。"),
        ],
        "keywords": ["investigadores", "señalar", "directivos", "permitirse", "fiarse", "intuición", "molestarse", "analizar", "datos", "incurrir", "sesgos"],
    },
    "M24-039": {
        "slash_es": "¿No te da vergüenza / haberte quejado tanto / de los problemas del sistema / sin haberte molestado / ni una sola vez / en presentar una propuesta alternativa / ante las autoridades?",
        "breakdown": [
            ("句型結構", "否定疑問句（¿No te da vergüenza...?）使用 dar vergüenza + inf. 完成式，表達對聽者的道德質疑，含 sin + inf. 完成式的否定伴隨狀語。"),
            ("片語拆解", "dar vergüenza + inf.：固定結構，表示感到羞恥於做某事，使用不定詞完成式（haber + 過去分詞）表示過去行為。"),
            ("片語拆解", "quejarse de：動詞 quejarse 後接介詞 de，表示抱怨某事。"),
            ("片語拆解", "molestarse en + inf.：表示費心去做某事，否定形式表示懶得做某事。"),
            ("片語拆解", "presentar ante：動詞 presentar 後接 ante，表示向某機構或人員提交。"),
            ("語法細節", "sin haberte molestado 使用不定詞完成式（haber + 過去分詞），表示在過去某時間段內未曾做過的事，與主句的 haberte quejado 時態相呼應。"),
        ],
        "keywords": ["vergüenza", "quejarse", "sistema", "molestarse", "presentar", "propuesta", "alternativa", "autoridades"],
    },
    "M24-040": {
        "slash_es": "Me avergüenza reconocerlo, / pero tienes razón: / me he limitado / a criticar / sin atreverme / a arriesgarme / a ofrecer soluciones / porque me aterra / que se rían de mis ideas.",
        "breakdown": [
            ("句型結構", "自我反省句，以 pero 轉折承認對方說得對；後半句說明原因，含兩個 sin + inf. 的否定伴隨狀語，末尾以 porque 引導原因從句。"),
            ("片語拆解", "avergonzarse de + inf.：以做某事為恥，此處 me avergüenza 為使役結構（某事令我感到羞愧）。"),
            ("片語拆解", "limitarse a + inf.：表示只是做某事，帶有限縮範疇的含義。"),
            ("片語拆解", "atreverse a + inf.：表示敢於做某事，此處為否定形式。"),
            ("片語拆解", "arriesgarse a + inf.：表示冒著做某事的風險。"),
            ("語法細節", "que se rían de mis ideas：que 引導的名詞子句作 aterra 的受詞，se rían 為虛擬式，因為 aterrar que 表達情感。"),
        ],
        "keywords": ["avergonzar", "reconocer", "razón", "limitarse", "criticar", "atreverse", "arriesgarse", "ofrecer", "soluciones", "ideas"],
    },
    "M24-041": {
        "slash_es": "¿Cómo te las arreglas / para no avergonzarte / de tus errores pasados / y seguir atreviéndote / a tomar decisiones arriesgadas / en un entorno / tan competitivo?",
        "breakdown": [
            ("句型結構", "cómo 引導方式疑問句，動詞為 arreglárselas para，後接兩個並列不定詞（no avergonzarte 和 seguir atreviéndote），形成並列結構。"),
            ("片語拆解", "arreglárselas para + inf.：固定片語，表示設法做到某事，帶有克服困難的含義。"),
            ("片語拆解", "avergonzarse de：表示以某事為恥或感到羞愧。"),
            ("片語拆解", "seguir + 現在分詞：動詞 seguir 後接現在分詞，表示繼續做某事。"),
            ("片語拆解", "atreverse a + inf.：表示敢於做某事。"),
        ],
        "keywords": ["arreglárselas", "avergonzarse", "errores", "pasados", "seguir", "atreverse", "decisiones", "arriesgadas", "entorno", "competitivo"],
    },
    "M24-042": {
        "slash_es": "Intento acordarme de / que cada error / me ha permitido / aprender algo valioso, / así que en vez de / avergonzarme, / procuro alegrarme de / cada experiencia vivida.",
        "breakdown": [
            ("句型結構", "主句為「Intento acordarme de que...」，que 引導名詞子句；así que 引導結果從句，含 en vez de 對比結構。"),
            ("片語拆解", "acordarse de + que 子句：動詞 acordarse 後接介詞 de，再接 que 從句，表示記得某事。"),
            ("片語拆解", "permitir + inf.：動詞 permitir 後直接接不定詞，表示允許或使得做某事成為可能。"),
            ("片語拆解", "en vez de + inf.：表示「而非」。"),
            ("片語拆解", "avergonzarse（de）：表示以某事為恥。"),
            ("片語拆解", "procurar + inf.：動詞 procurar 後直接接不定詞，表示努力設法做某事。"),
            ("片語拆解", "alegrarse de：表示為某事感到高興。"),
        ],
        "keywords": ["acordarse", "error", "permitir", "aprender", "avergonzarse", "procurar", "alegrarse", "experiencia"],
    },
    "M24-043": {
        "slash_es": "Es muy saludable / que logres alegrarte / de tus fracasos / en vez de / paralizarte por ellos; / la clave / está en acordarse de / que el error / forma parte / del proceso de aprendizaje.",
        "breakdown": [
            ("句型結構", "前半句為「Es + 形容詞 + que + 虛擬式」評價結構，含 en vez de 對比；後半句以分號連接，提出核心觀點（la clave está en...）。"),
            ("片語拆解", "lograr + inf.：表示成功做到某事。"),
            ("片語拆解", "alegrarse de：表示為某事感到高興。"),
            ("片語拆解", "en vez de + inf.：表示「而非」。"),
            ("片語拆解", "paralizarse por：動詞 paralizarse 後接介詞 por，表示被某事所癱瘓或阻礙。"),
            ("片語拆解", "la clave está en + inf.：固定表達，表示關鍵在於做某事。"),
            ("片語拆解", "acordarse de + que 子句：表示記得某事。"),
            ("語法細節", "logres 為虛擬式，因主句為非人稱評價（Es muy saludable que）。"),
        ],
        "keywords": ["saludable", "lograr", "alegrarse", "fracasos", "paralizarse", "clave", "acordarse", "error", "aprendizaje"],
    },
    "M24-044": {
        "slash_es": "Un coach empresarial subraya / que los líderes más resilientes / son los que logran / acordarse de sus fracasos / sin avergonzarse de ellos / y alegrarse de los aprendizajes / sin enorgullecerse en exceso.",
        "breakdown": [
            ("句型結構", "主句為「Un coach...subraya que...」，que 從句中用關係子句（los que logran...）限定主語，後跟兩組對比的 sin 結構（sin avergonzarse... / sin enorgullecerse...）。"),
            ("片語拆解", "subrayar que：動詞 subrayar 後接 que 從句，表示強調某事。"),
            ("片語拆解", "lograr + inf.：表示成功做到某事。"),
            ("片語拆解", "acordarse de：表示記得或想起某事。"),
            ("片語拆解", "avergonzarse de：表示以某事為恥。"),
            ("片語拆解", "alegrarse de：表示為某事感到高興。"),
            ("片語拆解", "enorgullecerse de（en exceso）：動詞 enorgullecerse 後接介詞 de，表示為某事感到自豪，en exceso 修飾過度程度。"),
        ],
        "keywords": ["coach", "subrayar", "líderes", "resilientes", "lograr", "acordarse", "fracasos", "avergonzarse", "alegrarse", "aprendizajes", "enorgullecerse"],
    },
    "M24-045": {
        "slash_es": "¿Cómo haces / para acordarte / de mantener la calma / cuando te enfrentas / a situaciones / en las que todo parece / desmoronarse a la vez?",
        "breakdown": [
            ("句型結構", "cómo 引導方式疑問句，動詞為 hacer para，後接 acordarte de + inf. 結構；when 從句（cuando）限定情況，情況中含關係子句（en las que）。"),
            ("片語拆解", "hacer para + inf.：非正式固定表達，表示如何設法做某事（口語中 hacer 代替 arreglárselas）。"),
            ("片語拆解", "acordarse de + inf.：表示記得要做某事。"),
            ("片語拆解", "enfrentarse a：動詞 enfrentarse 後接介詞 a，表示面對或應對某事。"),
            ("語法細節", "en las que todo parece desmoronarse 為關係子句，介詞 en 提前，修飾前面的 situaciones。"),
        ],
        "keywords": ["acordarse", "mantener", "calma", "enfrentarse", "situaciones", "parecer", "desmoronarse"],
    },
    "M24-046": {
        "slash_es": "Me ayuda / acordarme de / que he superado crisis anteriores; / además, / procuro enfocarme / en lo que puedo controlar / en vez de / angustiarme / por lo que no depende de mí.",
        "breakdown": [
            ("句型結構", "前半句以 Me ayuda + inf. 說明有效策略，後半句以 además 遞進，含 en vez de 對比結構。"),
            ("片語拆解", "ayudar + inf.：動詞 ayudar 後直接接不定詞，表示做某事有幫助（非人稱結構）。"),
            ("片語拆解", "acordarse de + que 子句：表示記得某事。"),
            ("片語拆解", "procurar + inf.：表示努力設法做某事。"),
            ("片語拆解", "enfocarse en：動詞 enfocarse 後接介詞 en，表示專注於某事。"),
            ("片語拆解", "en vez de + inf.：表示「而非」。"),
            ("片語拆解", "angustiarse por：動詞 angustiarse 後接介詞 por，表示為某事感到焦慮。"),
            ("片語拆解", "depender de：表示依賴或取決於某人或某事。"),
        ],
        "keywords": ["ayudar", "acordarse", "superar", "crisis", "procurar", "enfocarse", "controlar", "angustiarse", "depender"],
    },
    "M24-047": {
        "slash_es": "Es admirable / que hayas aprendido / a enfocarte en lo que puedes controlar; / muchos se obsesionan / con preocuparse por / lo incontrolable / en vez de / centrarse / en actuar con sensatez.",
        "breakdown": [
            ("句型結構", "前半句為「Es + 形容詞 + que + 虛擬式完成時」的評價結構；後半句以 muchos 作主語做對比描述，含 en vez de 結構。"),
            ("片語拆解", "enfocarse en：表示專注於某事。"),
            ("片語拆解", "obsesionarse con + inf./名詞：動詞 obsesionarse 後接介詞 con，表示執著或沉迷於某事。"),
            ("片語拆解", "preocuparse por：表示擔心或在意某事。"),
            ("片語拆解", "en vez de + inf.：表示「而非」。"),
            ("片語拆解", "centrarse en + inf.：表示專注於做某事。"),
            ("語法細節", "hayas aprendido 為虛擬式完成時（pretérito perfecto de subjuntivo），因主句為評價句（Es admirable que），且事件發生在說話之前。"),
        ],
        "keywords": ["admirable", "aprender", "enfocarse", "controlar", "obsesionarse", "preocuparse", "incontrolable", "centrarse", "actuar", "sensatez"],
    },
    "M24-048": {
        "slash_es": "Estudios sobre inteligencia emocional confirman / que las personas que logran / enfocarse en soluciones / sin obsesionarse / con los problemas / tienden a recuperarse / más rápidamente / de la adversidad.",
        "breakdown": [
            ("句型結構", "主句為「Estudios...confirman que...」，que 從句主語為帶關係子句的名詞短語（las personas que logran...），謂語為 tienden a recuperarse。"),
            ("片語拆解", "lograr + inf.：表示成功做到某事。"),
            ("片語拆解", "enfocarse en：表示專注於某事。"),
            ("片語拆解", "obsesionarse con：表示執著或沉迷於某事，否定形式 sin obsesionarse 表示不過度執著。"),
            ("片語拆解", "tender a + inf.：表示傾向於做某事。"),
            ("片語拆解", "recuperarse de：動詞 recuperarse 後接介詞 de，表示從某事中恢復。"),
        ],
        "keywords": ["estudios", "inteligencia", "emocional", "confirmar", "personas", "lograr", "enfocarse", "soluciones", "obsesionarse", "tender", "recuperarse", "adversidad"],
    },
    "M24-049": {
        "slash_es": "¿No te arrepientes / de haber malgastado / tantos años obsesionándote / con la opinión ajena / en vez de / haberte atrevido / a perseguir / tus propias metas / con convicción?",
        "breakdown": [
            ("句型結構", "否定疑問句（¿No te arrepientes de...?）以 haber + 過去分詞完成式表達對過去行為的後悔，含 en vez de 對比結構。"),
            ("片語拆解", "arrepentirse de + haber + 過去分詞：表示後悔曾做過某事。"),
            ("片語拆解", "malgastar：動詞 malgastar 表示浪費時間或資源。"),
            ("片語拆解", "obsesionarse con：表示執著或沉迷於某事，此處用現在分詞 obsesionándote 表示伴隨狀態。"),
            ("片語拆解", "en vez de + haber + 過去分詞：en vez de 後接不定詞完成式，表示對比過去另一種本可採取的行動。"),
            ("片語拆解", "atreverse a + inf.：表示敢於做某事。"),
            ("片語拆解", "perseguir：動詞表示追求或追逐某目標。"),
        ],
        "keywords": ["arrepentirse", "malgastar", "años", "obsesionarse", "opinión", "atreverse", "perseguir", "metas", "convicción"],
    },
    "M24-050": {
        "slash_es": "En cierta medida sí; / me he dado cuenta de / que pasé demasiado tiempo / preocupándome por / lo que pensaban los demás / en lugar de / atreverme / a construir algo / que realmente me apasionara.",
        "breakdown": [
            ("句型結構", "前半句部分認同（En cierta medida sí），後半句以 darse cuenta de que 引導反思，que 從句含 en lugar de 對比結構。"),
            ("片語拆解", "darse cuenta de + que 子句：固定片語，表示意識到或發現某事。"),
            ("片語拆解", "pasar tiempo + 現在分詞：固定結構，表示花費時間做某事。"),
            ("片語拆解", "preocuparse por：表示擔心或在意某事。"),
            ("片語拆解", "en lugar de + inf.：表示「而非」。"),
            ("片語拆解", "atreverse a + inf.：表示敢於做某事。"),
            ("語法細節", "me apasionara 為過去未完成虛擬式，因為其修飾的先行詞 algo 為不確定的假設性指涉（某個當時尚未建立的事物）。"),
        ],
        "keywords": ["medida", "darse", "cuenta", "pasar", "tiempo", "preocuparse", "demás", "atreverse", "construir", "apasionar"],
    },
}

def convert_id(old_id):
    """Convert M24-001 to M6-W24-001"""
    parts = old_id.split("-")
    num = parts[1]
    return f"M6-W24-{num}"

def get_type_label(t):
    return t

def format_card(row_type, old_id, es, zh, grammar, analysis):
    new_id = convert_id(old_id)

    slash_es = analysis["slash_es"]
    breakdown = analysis["breakdown"]
    keywords = analysis["keywords"]

    lines = []
    lines.append(f"Q | {new_id}")
    lines.append("")
    lines.append(f"ES：{slash_es}")
    lines.append(f"ZH：{zh}")
    lines.append(f"核心語法：{grammar}")
    lines.append("拆解：")
    for tag, text in breakdown:
        lines.append(f"【{tag}】{text}")

    kw_links = " ".join(f"[[{k}]]" for k in keywords)
    lines.append(f"核心單字：{kw_links}")

    return "\n".join(lines)

def main():
    wb = openpyxl.load_workbook("/home/user/48wk_spanish/WK24.xlsx")
    ws = wb.active

    data = []
    for row in ws.iter_rows(min_row=12, values_only=True):
        if row[0] and row[1]:
            data.append(row)

    output_dir = "/home/user/48wk_spanish/output3/M6-W24"
    os.makedirs(output_dir, exist_ok=True)

    index_rows = []
    count = 0

    for row in data:
        row_type = row[0]
        old_id = row[1]
        es = row[2] or ""
        zh = row[3] or ""
        grammar = row[4] or ""

        new_id = convert_id(old_id)

        if old_id in ANALYSIS:
            analysis = ANALYSIS[old_id]
            content = format_card(row_type, old_id, es, zh, grammar, analysis)
        else:
            # Fallback: generate basic card without detailed analysis
            content = f"Q | {new_id}\n\nES：{es}\nZH：{zh}\n核心語法：{grammar}\n拆解：\n【句型結構】（分析待補）\n核心單字："

        filepath = os.path.join(output_dir, f"{new_id}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        count += 1
        index_rows.append(f"| [[M6-W24/{new_id}]] | {row_type} | {grammar} |")

    # Determine topic from first few cards
    index_content = "# M6-W24 索引：社交媒體與隱私\n\n"
    index_content += "| 編號 | 類型 | 語法重點 |\n"
    index_content += "|---|---|---|\n"
    index_content += "\n".join(index_rows)
    index_content += "\n"

    index_path = "/home/user/48wk_spanish/output3/M6-W24_index.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)

    print(f"Generated {count} card files + 1 index file = {count + 1} total files")

if __name__ == "__main__":
    main()

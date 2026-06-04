#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openpyxl
import os

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
            ("句型結構", "主句為「El experto advierte de」，後接 que 引導的名詞子句作為 advertir de 的受詞，子句中包含目的不定詞短語。"),
            ("片語拆解", "advertir de + que 子句：動詞 advertir 後接介詞 de，再接 que 從句，表示提醒或警告某事。"),
            ("片語拆解", "carecer de：動詞 carecer 後接介詞 de，表示缺乏某物，為固定搭配。"),
            ("片語拆解", "para + inf.：表示目的，此處說明需要工具的用途。"),
            ("語法細節", "frente a 為介詞短語，表示面對或應對某事物，帶有對抗語義。"),
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
        "slash_es": "Sí, / me niego a aceptar / cualquier práctica / que atente contra el derecho / a la intimidad de las personas / sin su consentimiento explícito y firmado.",
        "breakdown": [
            ("句型結構", "主句為「me niego a aceptar」，受詞為名詞短語加關係子句（que atente contra...），sin 引導否定伴隨狀語。"),
            ("片語拆解", "negarse a + inf.：動詞 negarse 後接介詞 a，再加不定詞，表示拒絕做某事。"),
            ("片語拆解", "atentar contra：動詞 atentar 後接介詞 contra，表示侵犯或危害某事物。"),
            ("語法細節", "atente 為虛擬式，因為先行詞 práctica 指的是假設性的、不確定的行為，關係子句描述尚未確定的特徵。"),
        ],
        "keywords": ["negarse", "aceptar", "práctica", "atentar", "derecho", "intimidad", "personas", "consentimiento"],
    },
    "M24-007": {
        "slash_es": "¡Totalmente de acuerdo! / Las corporaciones deben preocuparse / por la ética digital / en lugar de centrarse únicamente / en maximizar sus beneficios económicos.",
        "breakdown": [
            ("句型結構", "感嘆式強調認同後，主句用 deber + inf. 表達應然義務，末尾以 en lugar de 對比結構說明錯誤做法。"),
            ("片語拆解", "preocuparse por：動詞 preocuparse 後接介詞 por，表示關注或在意某事。"),
            ("片語拆解", "en lugar de + inf.：表示「而非」，後接不定詞，用於對比兩種行為。"),
            ("片語拆解", "centrarse en + inf.：動詞 centrarse 後接介詞 en，再加不定詞，表示專注於做某事。"),
        ],
        "keywords": ["corporaciones", "preocuparse", "ética", "centrarse", "maximizar", "beneficios"],
    },
    "M24-008": {
        "slash_es": "Si los usuarios dependieran / de las redes sociales para informarse, / no tardarían / en caer en campañas de desinformación / diseñadas para manipular la opinión.",
        "breakdown": [
            ("句型結構", "整句為虛擬條件句（Si + 過去虛擬式 + 條件式），表示假設性情境，暗示現實中確有此類風險。"),
            ("片語拆解", "depender de：動詞 depender 後接介詞 de，表示依賴某人或某事物作為來源。"),
            ("片語拆解", "tardar en + inf.：動詞 tardar 後接介詞 en，再加不定詞，表示花時間做某事，否定形式（no tardar en）表示很快就會做某事。"),
            ("片語拆解", "caer en：動詞 caer 後接介詞 en，表示陷入某種不良狀態或情況。"),
            ("語法細節", "dependieran 為過去未完成虛擬式，tardarían 為條件式，構成二類條件句，表示與現實相反或假設性的情況。"),
        ],
        "keywords": ["usuarios", "depender", "redes", "sociales", "informarse", "tardar", "caer", "desinformación", "manipular"],
    },
    "M24-009": {
        "slash_es": "¿A quién recurrió el gerente de marketing / cuando se enteró de / que la cuenta oficial de la compañía / había sido hackeada / por un grupo anónimo?",
        "breakdown": [
            ("句型結構", "整句為 a quién 引導的特殊疑問句，問詢對象；cuando 引導時間從句，時間從句中又含 que 名詞子句。"),
            ("片語拆解", "recurrir a：動詞 recurrir 後接介詞 a，表示求助於某人或某機構。"),
            ("片語拆解", "enterarse de + que 子句：表示得知某事，de que 後接陳述式。"),
            ("語法細節", "había sido hackeada 為過去完成被動式（pluscuamperfecto pasivo），表示在 se enteró 之前已發生的被動事件。"),
        ],
        "keywords": ["recurrir", "gerente", "marketing", "enterarse", "cuenta", "compañía", "hackear", "grupo"],
    },
    "M24-010": {
        "slash_es": "Recurrió a una agencia especializada / en ciberseguridad, / la cual se encargó de restablecer el control / y de informar a los seguidores / sobre el incidente.",
        "breakdown": [
            ("句型結構", "主句後接 la cual 引導的非限定性關係子句補充說明機構的行動，兩個 de + inf. 並列說明其職責。"),
            ("片語拆解", "recurrir a：表示求助於某人或某機構。"),
            ("片語拆解", "especializarse en：動詞 especializarse（此處為形容詞形式 especializada）後接介詞 en，表示專攻某領域。"),
            ("片語拆解", "encargarse de + inf.：動詞 encargarse 後接介詞 de，再加不定詞，表示負責做某事。"),
            ("片語拆解", "informar a alguien sobre：動詞 informar 後接 a（對象）加 sobre（話題），表示就某事告知某人。"),
        ],
        "keywords": ["recurrir", "agencia", "especializada", "ciberseguridad", "encargarse", "restablecer", "control", "informar", "seguidores", "incidente"],
    },
    "M24-011": {
        "slash_es": "¿Cree usted / que el éxito de una campaña en redes / depende de la cantidad de datos personales / que la empresa logre recopilar / de sus clientes?",
        "breakdown": [
            ("句型結構", "整句為 creer que 引導的間接疑問句，que 後接名詞子句，子句中含 que 引導的限定性關係子句修飾 datos personales。"),
            ("片語拆解", "depender de：動詞 depender 後接介詞 de，表示取決於或依賴某事物。"),
            ("片語拆解", "lograr + inf.：動詞 lograr 後直接接不定詞，表示成功做到某事。"),
            ("片語拆解", "recopilar：動詞表示收集或彙整資料，為數位營銷常用詞彙。"),
        ],
        "keywords": ["creer", "éxito", "campaña", "redes", "depender", "datos", "personales", "lograr", "recopilar", "clientes"],
    },
    "M24-012": {
        "slash_es": "No del todo; / depende más de la creatividad del mensaje, / aunque reconozco / que segmentar el público / contribuye a mejorar / el impacto de la publicidad.",
        "breakdown": [
            ("句型結構", "以 No del todo 部分否定開頭，後接 aunque 讓步從句，構成「雖然…但主要…」的轉折讓步結構。"),
            ("片語拆解", "depender de：表示取決於某事物。"),
            ("片語拆解", "reconocer que：動詞 reconocer 後接 que 從句，表示承認某事為真。"),
            ("片語拆解", "contribuir a + inf.：動詞 contribuir 後接介詞 a，再加不定詞，表示有助於做某事。"),
        ],
        "keywords": ["depender", "creatividad", "mensaje", "reconocer", "segmentar", "público", "contribuir", "mejorar", "impacto", "publicidad"],
    },
    "M24-013": {
        "slash_es": "¡Es un dilema! / Me preocupa / que, por obsesionarse con las métricas, / muchas marcas terminen / por violar los límites / de la privacidad de los consumidores.",
        "breakdown": [
            ("句型結構", "感嘆句後接 preocupar que 情感結構，que 從句含 por + inf. 的原因短語，整句表達對某種趨勢的憂慮。"),
            ("片語拆解", "preocupar que + 虛擬式：動詞 preocupar 後接 que 從句，從句主詞不同時用虛擬式，表示某事令人擔憂。"),
            ("片語拆解", "obsesionarse con：動詞 obsesionarse 後接介詞 con，表示執著或沉迷於某事。"),
            ("片語拆解", "terminar por + inf.：動詞 terminar 後接介詞 por，再加不定詞，表示最終做了某事，含有漸進過程的語義。"),
            ("語法細節", "terminen 為虛擬式，因為整個 que 從句是 preocupar 所支配的情感受詞。"),
        ],
        "keywords": ["dilema", "preocupar", "obsesionarse", "métricas", "marcas", "terminar", "violar", "límites", "privacidad", "consumidores"],
    },
    "M24-014": {
        "slash_es": "El director general / se comprometió / a no vender la base de datos / a terceros, / insistiendo en / que la confianza del cliente / está por encima de todo.",
        "breakdown": [
            ("句型結構", "主句為「El director se comprometió a...」，後接現在分詞 insistiendo 作伴隨狀語，補充說明做出承諾時強調的理由。"),
            ("片語拆解", "comprometerse a + inf.：動詞 comprometerse 後接介詞 a，再加不定詞，表示承諾做某事。"),
            ("片語拆解", "insistir en + que 子句：動詞 insistir 後接介詞 en，再接 que 從句，表示堅持主張某事。"),
            ("片語拆解", "estar por encima de：固定片語，表示凌駕於或高於某事物。"),
        ],
        "keywords": ["director", "comprometerse", "vender", "datos", "terceros", "insistir", "confianza", "cliente"],
    },
    "M24-015": {
        "slash_es": "¿Por qué te sorprendes / de que el gobierno intente / regular las plataformas / si estas se niegan / a colaborar / en la lucha contra el cibercrimen?",
        "breakdown": [
            ("句型結構", "整句為特殊疑問句，主句為 sorprenderse de que + 虛擬式，後接 si 條件從句提供背景理由。"),
            ("片語拆解", "sorprenderse de que + 虛擬式：動詞 sorprenderse 後接介詞 de，再接 que 從句，從句動詞用虛擬式，表示對某事感到驚訝。"),
            ("片語拆解", "intentar + inf.：動詞 intentar 後直接接不定詞，表示試圖做某事。"),
            ("片語拆解", "negarse a + inf.：表示拒絕做某事。"),
            ("語法細節", "intente 為虛擬式，因為受 sorprenderse de que 情感動詞支配。"),
        ],
        "keywords": ["sorprenderse", "gobierno", "intentar", "regular", "plataformas", "negarse", "colaborar", "lucha", "cibercrimen"],
    },
    "M24-016": {
        "slash_es": "Me sorprendo de la falta de diálogo; / si ambas partes / se dedicaran / a buscar un consenso, / la privacidad del ciudadano / saldría muy beneficiada.",
        "breakdown": [
            ("句型結構", "前半句為感嘆式評論，後半句為 Si + 過去虛擬式 + 條件式的二類虛擬條件句，表示假設性理想情境。"),
            ("片語拆解", "sorprenderse de：動詞 sorprenderse 後接介詞 de，表示對某事感到驚訝。"),
            ("片語拆解", "dedicarse a + inf.：動詞 dedicarse 後接介詞 a，再加不定詞，表示致力於做某事。"),
            ("語法細節", "dedicaran 為過去未完成虛擬式，saldría 為條件式，構成二類條件句，表示與現實相反的假設。"),
        ],
        "keywords": ["sorprenderse", "diálogo", "partes", "dedicarse", "buscar", "consenso", "privacidad", "ciudadano"],
    },
    "M24-017": {
        "slash_es": "Tienes razón; / es hora de que las grandes tecnológicas / dejen de actuar / de forma unilateral / y empiecen / a respetar las leyes locales / de cada país.",
        "breakdown": [
            ("句型結構", "以「Tienes razón」表示認同，後接「es hora de que + 虛擬式」的固定時間評價結構，含兩個並列虛擬式動詞（dejen 和 empiecen）。"),
            ("片語拆解", "ser hora de que + 虛擬式：固定片語，表示是時候做某事了，que 後接虛擬式。"),
            ("片語拆解", "dejar de + inf.：動詞 dejar 後接介詞 de，再加不定詞，表示停止做某事。"),
            ("片語拆解", "empezar a + inf.：動詞 empezar 後接介詞 a，再加不定詞，表示開始做某事。"),
            ("語法細節", "dejen 和 empiecen 均為虛擬式，因受 es hora de que 支配。"),
        ],
        "keywords": ["razón", "tecnológicas", "dejar", "actuar", "unilateral", "empezar", "respetar", "leyes", "locales"],
    },
    "M24-018": {
        "slash_es": "Si la aplicación careciera / de un sistema de verificación en dos pasos, / los usuarios se expondrían / a que sus contraseñas / fueran robadas / con gran facilidad.",
        "breakdown": [
            ("句型結構", "Si + 過去虛擬式 + 條件式的二類條件句，假設應用程式缺乏某功能的後果；主句含 exponerse a que + 虛擬式的固定結構。"),
            ("片語拆解", "carecer de：動詞 carecer 後接介詞 de，表示缺乏某物。"),
            ("片語拆解", "exponerse a que + 虛擬式：動詞 exponerse 後接介詞 a，再接 que 從句，表示使自己暴露於某種風險，que 後動詞用虛擬式。"),
            ("語法細節", "careciera 為過去未完成虛擬式，expondrían 為條件式，構成二類條件句；fueran robadas 為過去未完成虛擬式被動式。"),
        ],
        "keywords": ["aplicación", "carecer", "sistema", "verificación", "usuarios", "exponerse", "contraseñas", "robar"],
    },
    "M24-019": {
        "slash_es": "¿De qué se quejan los usuarios / cuando la red social cambia / sus condiciones de servicio / sin avisar a la comunidad / con suficiente antelación?",
        "breakdown": [
            ("句型結構", "de qué 引導特殊疑問句，問詢抱怨的具體內容；cuando 引導時間從句補充情境，時間從句含 sin + inf. 否定伴隨狀語。"),
            ("片語拆解", "quejarse de：動詞 quejarse 後接介詞 de，表示抱怨某事。"),
            ("片語拆解", "avisar a alguien（con antelación）：動詞 avisar 後接 a（對象），con antelación 表示提前告知。"),
            ("片語拆解", "sin + inf.：表示不做某伴隨動作，此處 sin avisar 表示未事先告知。"),
        ],
        "keywords": ["quejarse", "usuarios", "redes", "cambiar", "condiciones", "servicio", "avisar", "comunidad", "antelación"],
    },
    "M24-020": {
        "slash_es": "Se quejan de la falta de transparencia, / argumentando / que la empresa se aprovecha / de la ambigüedad legal / para comercializar / sus fotos privadas.",
        "breakdown": [
            ("句型結構", "主句為「Se quejan de...」，後接現在分詞 argumentando 作伴隨狀語說明抱怨的理由，理由中含 para + inf. 目的結構。"),
            ("片語拆解", "quejarse de：表示抱怨某事，de 後接名詞短語（la falta de transparencia）。"),
            ("片語拆解", "aprovecharse de：動詞 aprovecharse 後接介詞 de，表示利用或趁機利用某事物。"),
            ("片語拆解", "para + inf.：表示目的，此處說明企業利用模糊地帶的目的。"),
        ],
        "keywords": ["quejarse", "transparencia", "argumentar", "empresa", "aprovecharse", "ambigüedad", "legal", "comercializar", "fotos"],
    },
    "M24-021": {
        "slash_es": "¿A qué se debe / que tantas personas sigan subiendo fotos / de sus hijos a internet / a pesar de que los expertos / advierten de los riesgos?",
        "breakdown": [
            ("句型結構", "a qué 引導特殊疑問句，問詢原因；主句為 deberse a que + 虛擬式的固定原因結構，末尾 a pesar de que 引導讓步從句。"),
            ("片語拆解", "deberse a que + 虛擬式：固定結構，表示某事是由於某原因，que 後動詞用虛擬式。"),
            ("片語拆解", "seguir + 現在分詞：動詞 seguir 後接現在分詞，表示繼續做某事。"),
            ("片語拆解", "advertir de：動詞 advertir 後接介詞 de，表示警告或提醒某事。"),
            ("片語拆解", "a pesar de que + 陳述式：表示儘管某事為真，後接陳述式（已知事實）。"),
            ("語法細節", "sigan subiendo 使用虛擬式，因受 deberse a que 固定結構支配。"),
        ],
        "keywords": ["deber", "personas", "seguir", "subir", "fotos", "hijos", "internet", "expertos", "advertir", "riesgos"],
    },
    "M24-022": {
        "slash_es": "Se debe a la necesidad de aprobación social; / muchos padres no se dan cuenta de / que están exponiendo / a los menores / a peligros digitales graves.",
        "breakdown": [
            ("句型結構", "前半句以 deberse a 回答前問，後半句以分號連接補充原因，含 darse cuenta de que 認知結構。"),
            ("片語拆解", "deberse a：表示歸因於某事，de 後接名詞或 que 從句。"),
            ("片語拆解", "darse cuenta de que + 陳述式：固定片語，表示意識到某事，de que 後接陳述式。"),
            ("片語拆解", "exponer a：動詞 exponer 後接介詞 a，表示使某人暴露於某種風險或情境中。"),
        ],
        "keywords": ["deber", "necesidad", "aprobación", "social", "padres", "darse", "cuenta", "exponer", "menores", "peligros"],
    },
    "M24-023": {
        "slash_es": "¡Es alarmante! / Es necesario / que las escuelas contribuyan / a educar a las familias / sobre cómo protegerse / de los depredadores en la red.",
        "breakdown": [
            ("句型結構", "感嘆句後接「Es necesario que + 虛擬式」的非人稱義務結構，que 從句中含目的不定詞短語（cómo protegerse）。"),
            ("片語拆解", "ser necesario que + 虛擬式：非人稱固定結構，表示有必要某事發生，que 後接虛擬式。"),
            ("片語拆解", "contribuir a + inf.：動詞 contribuir 後接介詞 a，再加不定詞，表示有助於做某事。"),
            ("片語拆解", "protegerse de：動詞 protegerse 後接介詞 de，表示保護自己免受某事物的侵害。"),
            ("語法細節", "contribuyan 為虛擬式，因受 Es necesario que 支配。"),
        ],
        "keywords": ["alarmante", "necesario", "escuelas", "contribuir", "educar", "familias", "protegerse", "depredadores", "red"],
    },
    "M24-024": {
        "slash_es": "El nuevo reglamento europeo / obliga a todas las empresas / a borrar los datos del usuario / si este insiste / en ejercer / su derecho al olvido digital.",
        "breakdown": [
            ("句型結構", "主句為「El reglamento obliga a... a + inf.」的雙重不定詞結構，後接 si 條件從句。"),
            ("片語拆解", "obligar a alguien a + inf.：動詞 obligar 後接 a（對象），再接 a + 不定詞（動作），表示迫使某人做某事。"),
            ("片語拆解", "insistir en + inf.：表示堅持做某事。"),
            ("片語拆解", "ejercer：動詞表示行使（權利或職能），常用於法律語境。"),
        ],
        "keywords": ["reglamento", "europeo", "obligar", "empresas", "borrar", "datos", "usuario", "insistir", "ejercer", "derecho", "olvido"],
    },
    "M24-025": {
        "slash_es": "¿Por qué te asustas / de que las aplicaciones / escuchen tus conversaciones / si tú mismo aceptaste los términos / al instalar el software?",
        "breakdown": [
            ("句型結構", "整句為特殊疑問句，主句含 asustarse de que + 虛擬式，後接 si 條件從句提供對比理由，帶有責問語氣。"),
            ("片語拆解", "asustarse de que + 虛擬式：動詞 asustarse 後接介詞 de，再接 que 從句，從句用虛擬式，表示對某事感到害怕。"),
            ("片語拆解", "al + inf.：固定時間結構，表示「在做某事的時候」或「一旦做了某事」。"),
            ("語法細節", "escuchen 為虛擬式，因受 asustarse de que 情感動詞支配；tú mismo 中 mismo 為強調用法。"),
        ],
        "keywords": ["asustarse", "aplicaciones", "escuchar", "conversaciones", "aceptar", "términos", "instalar", "software"],
    },
    "M24-026": {
        "slash_es": "Me asusto de / que no haya un control real; / nadie se detiene / a leer esos contratos tan largos / porque todos tenemos prisa / por usar la tecnología.",
        "breakdown": [
            ("句型結構", "前半句含 asustarse de que + 虛擬式，後半句以分號連接，用 nadie + 動詞 + 原因結構解釋社會現象。"),
            ("片語拆解", "asustarse de que + 虛擬式：表示對某事感到害怕，que 後動詞用虛擬式（haya）。"),
            ("片語拆解", "detenerse a + inf.：動詞 detenerse 後接介詞 a，再加不定詞，表示停下來做某事，含有刻意暫停的語義。"),
            ("片語拆解", "tener prisa por + inf.：固定片語，表示急著做某事。"),
            ("語法細節", "haya 為虛擬式，因受 asustarse de que 情感動詞支配。"),
        ],
        "keywords": ["asustarse", "control", "nadie", "detenerse", "leer", "contratos", "prisa", "tecnología"],
    },
    "M24-027": {
        "slash_es": "¡Ahí está el truco! / Las empresas se basan / en esa falta de tiempo / de los consumidores / para apoderarse / de una cantidad ingente / de datos privados.",
        "breakdown": [
            ("句型結構", "感嘆句點出核心策略，主句為「Las empresas se basan en...」，後接 para + inf. 表示目的。"),
            ("片語拆解", "basarse en：動詞 basarse 後接介詞 en，表示以某事物為基礎或依據。"),
            ("片語拆解", "para + inf.：表示目的，此處說明企業利用消費者缺乏時間的目的。"),
            ("片語拆解", "apoderarse de：動詞 apoderarse 後接介詞 de，表示奪取或掌控大量某物。"),
        ],
        "keywords": ["truco", "empresas", "basarse", "tiempo", "consumidores", "apoderarse", "datos", "privados"],
    },
    "M24-028": {
        "slash_es": "Si el comité de seguridad / no se hubiera encargado / de encriptar los archivos confidenciales, / hoy estaríamos sufriendo / por una demanda millonaria / de los clientes.",
        "breakdown": [
            ("句型結構", "整句為三類條件句（Si + 過去完成虛擬式 + 條件完成式），表示與過去事實相反的假設；hoy 暗示後果延伸至現在。"),
            ("片語拆解", "encargarse de + inf.：表示負責做某事，動詞後接介詞 de 加不定詞。"),
            ("片語拆解", "sufrir por：表示因某事而受苦或蒙受損失。"),
            ("語法細節", "hubiera encargado 為過去完成虛擬式（pluscuamperfecto de subjuntivo），estaríamos sufriendo 為條件進行式，hoy 使後果更具有當下感。"),
        ],
        "keywords": ["comité", "seguridad", "encargarse", "encriptar", "archivos", "confidenciales", "sufrir", "demanda", "clientes"],
    },
    "M24-029": {
        "slash_es": "¿En qué consiste / la nueva función de privacidad / que la plataforma ha anunciado / esta mañana / para competir / con las aplicaciones de mensajería encriptada?",
        "breakdown": [
            ("句型結構", "en qué 引導特殊疑問句，問詢事物的具體內容；主句動詞為 consistir en，關係子句修飾名詞 función，末尾 para + inf. 表示目的。"),
            ("片語拆解", "consistir en：動詞 consistir 後接介詞 en，表示某事物的內容或本質在於某事，為定義性表達。"),
            ("片語拆解", "para + inf.：表示目的，此處說明推出新功能的商業目的。"),
            ("片語拆解", "competir con：動詞 competir 後接介詞 con，表示與某對手競爭。"),
        ],
        "keywords": ["consistir", "función", "privacidad", "plataforma", "anunciar", "competir", "aplicaciones", "mensajería", "encriptada"],
    },
    "M24-030": {
        "slash_es": "Consiste en la destrucción automática / de los mensajes / después de ser leídos, / impidiendo así / que nadie se apodere / de la información del chat.",
        "breakdown": [
            ("句型結構", "主句以 consistir en + 名詞短語定義功能，後接現在分詞 impidiendo 作結果伴隨狀語，含 que + 虛擬式的否定目的結構。"),
            ("片語拆解", "consistir en：表示某事物的本質在於某事。"),
            ("片語拆解", "después de + ser + 過去分詞：表示在被做某事之後，為被動不定詞時間結構。"),
            ("片語拆解", "impedir que + 虛擬式：動詞 impedir 後接 que 從句，從句動詞用虛擬式，表示阻止某事發生。"),
            ("片語拆解", "apoderarse de：表示奪取或掌控某物。"),
            ("語法細節", "se apodere 為虛擬式，因受 impidiendo que 阻止性動詞支配。"),
        ],
        "keywords": ["consistir", "destrucción", "mensajes", "leídos", "impedir", "apoderarse", "información", "chat"],
    },
    "M24-031": {
        "slash_es": "¿Le importaría decirme / si usted confía / en que las leyes de protección de datos actuales / son suficientes / para frenar los abusos / de las grandes corporaciones?",
        "breakdown": [
            ("句型結構", "以條件式 importaría 開頭的禮貌請求（¿Le importaría + inf.?），後接間接疑問句 si + 陳述式，詢問對方的看法。"),
            ("片語拆解", "importar + inf.：動詞 importar 用條件式（importaría）加不定詞，構成禮貌詢問句型（¿Le importaría...?）。"),
            ("片語拆解", "confiar en que + 陳述式：動詞 confiar 後接介詞 en，再接 que 從句，表示相信某事為真。"),
            ("片語拆解", "para + inf.：表示目的，說明法律的預期功效。"),
        ],
        "keywords": ["importar", "decir", "confiar", "leyes", "protección", "datos", "suficientes", "frenar", "abusos", "corporaciones"],
    },
    "M24-032": {
        "slash_es": "Sinceramente, / no confío en ellas; / las leyes siempre tardan / en adaptarse / a las nuevas tecnologías, / dejando a los ciudadanos / desprotegidos / ante el avance digital.",
        "breakdown": [
            ("句型結構", "前半句為直接否定表態，後半句以分號連接，用普遍性陳述（las leyes siempre tardan...）加現在分詞 dejando 作伴隨結果狀語。"),
            ("片語拆解", "confiar en：表示信任某人或某事物。"),
            ("片語拆解", "tardar en + inf.：動詞 tardar 後接介詞 en，再加不定詞，表示在做某事上花費時間，或遲遲才做某事。"),
            ("片語拆解", "adaptarse a：動詞 adaptarse 後接介詞 a，表示適應某事物。"),
            ("片語拆解", "dejar a alguien + 形容詞/狀態：動詞 dejar 後接受詞加形容詞，表示使某人處於某種狀態。"),
        ],
        "keywords": ["confiar", "leyes", "tardar", "adaptarse", "tecnologías", "ciudadanos", "desprotegidos", "avance"],
    },
    "M24-033": {
        "slash_es": "Es una triste realidad; / por eso, / muchos usuarios optan por / cerrar sus perfiles / y alejarse de la vida digital activa / como medida de precaución.",
        "breakdown": [
            ("句型結構", "前半句為評論性陳述，por eso 承接前因引出結果，主句含 optar por + inf. 的選擇結構，後接並列不定詞。"),
            ("片語拆解", "optar por + inf.：動詞 optar 後接介詞 por，再加不定詞，表示選擇做某事。"),
            ("片語拆解", "alejarse de：動詞 alejarse 後接介詞 de，表示遠離或脫離某事物。"),
            ("片語拆解", "como medida de：固定短語，表示「作為某種手段/措施」。"),
        ],
        "keywords": ["realidad", "usuarios", "optar", "cerrar", "perfiles", "alejarse", "vida", "precaución"],
    },
    "M24-034": {
        "slash_es": "El hacker se aprovechó / de una vulnerabilidad / en el sistema operativo, / logrando acceder / al servidor / donde la empresa almacenaba / los datos de pago.",
        "breakdown": [
            ("句型結構", "主句為「El hacker se aprovechó de...」，後接現在分詞 logrando 作結果伴隨狀語，描述利用漏洞後達到的結果，含定語從句（donde...）。"),
            ("片語拆解", "aprovecharse de：動詞 aprovecharse 後接介詞 de，表示利用某漏洞或機會。"),
            ("片語拆解", "lograr + inf.：動詞 lograr 後直接接不定詞，表示成功做到某事，此處以現在分詞形式 logrando 作狀語。"),
            ("片語拆解", "acceder a：動詞 acceder 後接介詞 a，表示進入或存取某系統或地點。"),
        ],
        "keywords": ["hacker", "aprovecharse", "vulnerabilidad", "sistema", "operativo", "lograr", "acceder", "servidor", "empresa", "almacenar", "datos"],
    },
    "M24-035": {
        "slash_es": "¿Cómo reaccionó el director / cuando se enteró / de que las fotos del prototipo secreto / estaban circulando / por canales de comunicación no oficiales?",
        "breakdown": [
            ("句型結構", "cómo 引導方式疑問句，cuando 引導時間從句，時間從句中含 enterarse de que + 陳述式的認知結構。"),
            ("片語拆解", "reaccionar：動詞表示做出反應，cómo reaccionó 問詢反應的方式。"),
            ("片語拆解", "enterarse de que + 陳述式：表示得知某事，de que 後接陳述式（已發生的事實）。"),
            ("片語拆解", "circular por：動詞 circular 後接介詞 por，表示在某通道或渠道中流通傳播。"),
        ],
        "keywords": ["reaccionar", "director", "enterarse", "fotos", "prototipo", "secreto", "circular", "canales", "comunicación"],
    },
    "M24-036": {
        "slash_es": "Se enfadó con el equipo de desarrollo, / acusándolos / de haber sido descuidados / y de no haber cumplido / con las normas básicas / de confidencialidad de la firma.",
        "breakdown": [
            ("句型結構", "主句為「Se enfadó con...」，後接現在分詞 acusándolos 作伴隨動作狀語，描述憤怒的表現方式，含兩個並列的 de + 不定詞完成式結構。"),
            ("片語拆解", "enfadarse con：動詞 enfadarse 後接介詞 con，表示對某人感到憤怒。"),
            ("片語拆解", "acusar a alguien de + haber + 過去分詞：動詞 acusar 後接 a（對象）加 de + 不定詞完成式，表示指責某人曾做過某事。"),
            ("片語拆解", "cumplir con：動詞 cumplir 後接介詞 con，表示遵守或履行某規定或義務。"),
        ],
        "keywords": ["enfadarse", "equipo", "desarrollo", "acusar", "descuidados", "cumplir", "normas", "confidencialidad"],
    },
    "M24-037": {
        "slash_es": "¡Qué situación tan tensa! / Me imagino / que el responsable del descuido / se arrepentirá / de no haber guardado / el material / en la caja fuerte digital.",
        "breakdown": [
            ("句型結構", "感嘆句開頭表達情緒，主句為 imaginarse que + 陳述式，表示主觀推測，que 從句含 arrepentirse de + 不定詞完成式。"),
            ("片語拆解", "imaginarse que + 陳述式：動詞 imaginarse 後接 que 從句，表示想像或推測某事。"),
            ("片語拆解", "arrepentirse de + haber + 過去分詞：動詞 arrepentirse 後接 de + 不定詞完成式，表示後悔未曾做過某事。"),
            ("片語拆解", "guardar en：動詞 guardar 後接介詞 en，表示將某物保存於某處。"),
        ],
        "keywords": ["imaginar", "responsable", "descuido", "arrepentirse", "guardar", "material", "caja", "fuerte"],
    },
    "M24-038": {
        "slash_es": "Si la red social nos obligara / a rellenar un cuestionario / sobre nuestra vida privada, / muchos de nosotros / dejaríamos / de usar la aplicación / de inmediato.",
        "breakdown": [
            ("句型結構", "Si + 過去虛擬式 + 條件式的二類條件句，表示假設性情境及其後果。"),
            ("片語拆解", "obligar a alguien a + inf.：動詞 obligar 後接 a（對象）加 a + 不定詞，表示強迫某人做某事。"),
            ("片語拆解", "rellenar：動詞表示填寫表格或問卷。"),
            ("片語拆解", "dejar de + inf.：動詞 dejar 後接介詞 de，再加不定詞，表示停止做某事。"),
            ("語法細節", "obligara 為過去未完成虛擬式，dejaríamos 為條件式，構成二類條件句，表示假設性情況。"),
        ],
        "keywords": ["redes", "obligar", "rellenar", "cuestionario", "privada", "dejar", "usar", "aplicación"],
    },
    "M24-039": {
        "slash_es": "¿De qué depende / que un usuario decida / borrar su huella digital / y desconectarse de internet / para siempre, / según las investigaciones más recientes?",
        "breakdown": [
            ("句型結構", "de qué 引導特殊疑問句，主句為「¿De qué depende que + 虛擬式?」的固定問詢原因結構，según 引導來源狀語。"),
            ("片語拆解", "depender de que + 虛擬式：動詞 depender 後接介詞 de，再接 que 從句，從句用虛擬式，表示某事取決於某條件。"),
            ("片語拆解", "borrar la huella digital：固定短語，表示刪除網路上的個人數位足跡。"),
            ("片語拆解", "desconectarse de：動詞 desconectarse 後接介詞 de，表示從某網路或平台斷線或退出。"),
            ("語法細節", "decida 為虛擬式，因受 depende de que 結構支配。"),
        ],
        "keywords": ["depender", "usuario", "decidir", "borrar", "huella", "digital", "desconectarse", "internet", "investigaciones"],
    },
    "M24-040": {
        "slash_es": "Depende sobre todo / de su nivel de saturación mental; / cuando la gente / se cansa de / recibir publicidad dirigida, / comienza a valorar más / su anonimato.",
        "breakdown": [
            ("句型結構", "前半句以 depende de 回答前問，後半句以分號連接，用 cuando 時間從句加主句描述行為規律。"),
            ("片語拆解", "depender de：表示取決於某事物。"),
            ("片語拆解", "cansarse de + inf.：動詞 cansarse 後接介詞 de，再加不定詞，表示對做某事感到厭倦。"),
            ("片語拆解", "comenzar a + inf.：動詞 comenzar 後接介詞 a，再加不定詞，表示開始做某事。"),
            ("片語拆解", "valorar：動詞表示重視或珍視某事物。"),
        ],
        "keywords": ["depender", "saturación", "mental", "cansarse", "publicidad", "comenzar", "valorar", "anonimato"],
    },
    "M24-041": {
        "slash_es": "¿Por qué el departamento legal / insiste en / que debemos pedir permiso por escrito / cada vez que queramos / publicar el testimonio / de un cliente en la web?",
        "breakdown": [
            ("句型結構", "整句為特殊疑問句，主句含 insistir en que + 虛擬式，que 從句中又含 cada vez que + 虛擬式的時間從句。"),
            ("片語拆解", "insistir en que + 虛擬式：動詞 insistir 後接介詞 en，再接 que 從句，從句動詞用虛擬式，表示堅持要求某事發生。"),
            ("片語拆解", "pedir permiso：固定短語，表示請求許可。"),
            ("片語拆解", "por escrito：固定副詞短語，表示以書面方式。"),
            ("語法細節", "queramos 為虛擬式，因為 cada vez que 引導的時間從句指向未來重複發生的情況，此時用虛擬式。"),
        ],
        "keywords": ["departamento", "legal", "insistir", "pedir", "permiso", "publicar", "testimonio", "cliente"],
    },
    "M24-042": {
        "slash_es": "Insisten en ello / para protegernos / de posibles demandas por derechos de imagen, / evitando de este modo / que la empresa / se vea envuelta / en litigios costosos.",
        "breakdown": [
            ("句型結構", "主句 Insisten en ello 後接 para + inf. 目的結構，再以現在分詞 evitando 引導結果伴隨狀語，含 que + 虛擬式的防止結構。"),
            ("片語拆解", "insistir en ello：用代詞 ello 回指前文內容。"),
            ("片語拆解", "para + inf.：表示目的，說明堅持要求的理由。"),
            ("片語拆解", "evitar que + 虛擬式：動詞 evitar 後接 que 從句，從句動詞用虛擬式，表示避免某事發生。"),
            ("片語拆解", "verse envuelto en：固定片語，表示捲入某糾紛或事件。"),
        ],
        "keywords": ["insistir", "proteger", "demandas", "derechos", "imagen", "evitar", "empresa", "envuelta", "litigios"],
    },
    "M24-043": {
        "slash_es": "Me parece una excelente estrategia preventiva; / es mejor dedicar tiempo / a conseguir las autorizaciones correctas / que sufrir por / un error legal evitable.",
        "breakdown": [
            ("句型結構", "前半句為評論，後半句以 es mejor...que... 的比較結構對比兩種行為選擇（主動預防 vs. 被動受苦）。"),
            ("片語拆解", "parecer + 名詞短語：動詞 parecer 後接名詞短語，表示覺得某事物怎麼樣。"),
            ("片語拆解", "es mejor + inf. + que + inf.：固定比較結構，表示做某事比做另一件事更好。"),
            ("片語拆解", "dedicar tiempo a + inf.：表示花時間做某事。"),
            ("片語拆解", "conseguir + inf.：動詞 conseguir 後直接接不定詞，表示設法獲得或達成某事。"),
            ("片語拆解", "sufrir por：表示因某事而受苦或蒙受損失。"),
        ],
        "keywords": ["parecer", "estrategia", "preventiva", "dedicar", "tiempo", "conseguir", "autorizaciones", "sufrir", "error", "legal"],
    },
    "M24-044": {
        "slash_es": "El nuevo buscador / se caracteriza por / no almacenar el historial de navegación, / ofreciendo un entorno seguro / para quienes huyen / de la vigilancia comercial.",
        "breakdown": [
            ("句型結構", "主句為「El buscador se caracteriza por + inf.」，後接現在分詞 ofreciendo 作伴隨狀語，末尾 para quienes 引導目的關係子句。"),
            ("片語拆解", "caracterizarse por + inf.：動詞 caracterizarse 後接介詞 por，再加不定詞或名詞，表示以某特徵著稱。"),
            ("片語拆解", "almacenar：動詞表示儲存或保存資料。"),
            ("片語拆解", "para quienes + 動詞：表示「為那些…的人」，quienes 為關係代詞。"),
            ("片語拆解", "huir de：動詞 huir 後接介詞 de，表示逃避或遠離某事物。"),
        ],
        "keywords": ["buscador", "caracterizarse", "almacenar", "historial", "navegación", "entorno", "quienes", "huir", "vigilancia", "comercial"],
    },
    "M24-045": {
        "slash_es": "¿A qué se arriesga / una corporación / si se descubre / que vende los datos confidenciales / de sus usuarios / a agencias de marketing / sin autorización?",
        "breakdown": [
            ("句型結構", "a qué 引導特殊疑問句，問詢風險的具體內容；si 引導條件從句，從句中含 que 名詞子句作 descubrirse 的主語。"),
            ("片語拆解", "arriesgarse a：動詞 arriesgarse 後接介詞 a，表示面臨某種風險（此處為問句形式）。"),
            ("片語拆解", "descubrirse que：動詞 descubrirse（非人稱）後接 que 從句，表示被發現某事為真。"),
            ("片語拆解", "sin + 名詞：表示缺少某事物的伴隨狀態，sin autorización 表示未經授權。"),
        ],
        "keywords": ["arriesgarse", "corporación", "descubrir", "vender", "datos", "confidenciales", "usuarios", "agencias", "marketing", "autorización"],
    },
    "M24-046": {
        "slash_es": "Se arriesga a / multas multimillonarias / que podrían llevarla a la quiebra, / además de a / una pérdida irreparable de reputación / que la destruiría comercialmente.",
        "breakdown": [
            ("句型結構", "主句以 arriesgarse a 接名詞短語作受詞，後接關係子句（que podrían...），再以 además de a 並列另一風險。"),
            ("片語拆解", "arriesgarse a + 名詞：動詞 arriesgarse 後接介詞 a，再接名詞，表示面臨某種具體風險。"),
            ("片語拆解", "llevar a la quiebra：固定片語，表示導致破產。"),
            ("片語拆解", "además de a + 名詞：表示「除此之外還有…」，a 為介詞，接名詞短語。"),
        ],
        "keywords": ["arriesgarse", "multas", "llevar", "quiebra", "pérdida", "reputación", "destruir", "comercialmente"],
    },
    "M24-047": {
        "slash_es": "¡Es el castigo que se merecen! / Ninguna empresa debería aprovecharse / de la buena fe de las personas / para lucrarse / a costa de su intimidad protegida.",
        "breakdown": [
            ("句型結構", "感嘆句後接義務否定句（Ninguna empresa debería...），用 para + inf. 表示目的，a costa de 表示代價。"),
            ("片語拆解", "merecer：動詞表示應得或值得某種結果，此處為反身動詞 merecerse。"),
            ("片語拆解", "aprovecharse de：動詞 aprovecharse 後接介詞 de，表示利用某事物或某人。"),
            ("片語拆解", "para + inf.：表示目的。"),
            ("片語拆解", "lucrarse：動詞表示謀取私利或從中獲利。"),
            ("片語拆解", "a costa de：固定介詞短語，表示「以…為代價」。"),
        ],
        "keywords": ["castigo", "merecer", "empresa", "aprovecharse", "buena", "fe", "personas", "lucrarse", "intimidad"],
    },
    "M24-048": {
        "slash_es": "Si el administrador de la red / se hubiera fijado / en el tráfico inusual del servidor, / el robo de las cuentas / se habría evitado / antes de que fuera tarde.",
        "breakdown": [
            ("句型結構", "整句為三類條件句（Si + 過去完成虛擬式 + 條件完成式），表示與過去事實相反的假設，末尾 antes de que 引導時間從句。"),
            ("片語拆解", "fijarse en：動詞 fijarse 後接介詞 en，表示注意到或留意某事物。"),
            ("片語拆解", "evitarse（被動）：動詞 evitar 的被動反身形式，表示被避免。"),
            ("片語拆解", "antes de que + 虛擬式：表示「在某事發生之前」，que 後接虛擬式。"),
            ("語法細節", "hubiera fijado 為過去完成虛擬式，habría evitado 為條件完成式，fuera 為過去未完成虛擬式，三個時態共同構成三類條件句框架。"),
        ],
        "keywords": ["administrador", "red", "fijarse", "tráfico", "inusual", "servidor", "robo", "cuentas", "evitar"],
    },
    "M24-049": {
        "slash_es": "¿Usted cree / que para el final de esta década / la sociedad habrá aprendido / a convivir con la inteligencia artificial / sin renunciar / a la privacidad individual?",
        "breakdown": [
            ("句型結構", "整句為 creer que 引導的間接疑問句，que 從句含未來完成時（habrá aprendido），加 sin + inf. 的否定伴隨狀語。"),
            ("片語拆解", "creer que + 陳述式：動詞 creer 後接 que 從句，表示相信或認為某事。"),
            ("片語拆解", "aprender a + inf.：動詞 aprender 後接介詞 a，再加不定詞，表示學會做某事。"),
            ("片語拆解", "convivir con：動詞 convivir 後接介詞 con，表示與某事物共存或共處。"),
            ("片語拆解", "renunciar a：動詞 renunciar 後接介詞 a，表示放棄某權利或某事物。"),
            ("語法細節", "habrá aprendido 為未來完成時（futuro perfecto），表示到某未來時間點（el final de esta década）之前將已完成的動作。"),
        ],
        "keywords": ["creer", "sociedad", "aprender", "convivir", "inteligencia", "artificial", "renunciar", "privacidad"],
    },
    "M24-050": {
        "slash_es": "Ha sido un placer / debatir sobre estos temas; / si todos contribuimos / a exigir más transparencia, / lograremos / que el futuro digital / sea más respetuoso y seguro.",
        "breakdown": [
            ("句型結構", "前半句為感謝性總結，si 條件從句用陳述式（contribuimos）表示說話者認為條件可以實現；主句 lograremos 為未來時，含 que + 虛擬式的實現結構。"),
            ("片語拆解", "ser un placer + inf.：固定表達，表示做某事是一種愉快。"),
            ("片語拆解", "debatir sobre：動詞 debatir 後接介詞 sobre，表示就某話題進行辯論。"),
            ("片語拆解", "contribuir a + inf.：動詞 contribuir 後接介詞 a，再加不定詞，表示有助於做某事。"),
            ("片語拆解", "lograr que + 虛擬式：動詞 lograr 後接 que 從句，從句動詞用虛擬式，表示成功使某事發生。"),
            ("語法細節", "si + 陳述式現在時 + 未來時：表示說話者認為條件可以實現的一類條件句（若大家都貢獻→將會成功）；sea 為虛擬式，受 lograr que 支配。"),
        ],
        "keywords": ["placer", "debatir", "temas", "contribuir", "exigir", "transparencia", "lograr", "futuro", "digital", "respetuoso", "seguro"],
    },
}


def convert_id(old_id):
    parts = old_id.split("-")
    num = parts[1]
    return f"M6-W24-{num}"


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
            content = f"Q | {new_id}\n\nES：{es}\nZH：{zh}\n核心語法：{grammar}\n拆解：\n【句型結構】（分析待補）\n核心單字："

        filepath = os.path.join(output_dir, f"{new_id}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        count += 1
        index_rows.append(f"| [[M6-W24/{new_id}]] | {row_type} | {grammar} |")

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

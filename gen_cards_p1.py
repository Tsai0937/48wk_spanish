import os

OUT = "/home/user/48wk_spanish/output4"
os.makedirs(OUT, exist_ok=True)

def convert_id(old_id):
    num = old_id.split("-")[1]
    return f"M6-W24-{num}"

def write_card(new_id, card_type, es, zh, gram_title, parse_pts, gram_pts, keywords):
    fname = f"{OUT}/{new_id}.md"
    parse_block = "\n".join(f"{i+1}. {p}" for i, p in enumerate(parse_pts))
    gram_block = "\n".join(f"{i+1}. {g}" for i, g in enumerate(gram_pts))
    kw_block = " ".join(f"[[{w}]]" for w in keywords)
    content = f"""{card_type} | {new_id}

ES：{es}
ZH：{zh}
核心語法：{gram_title}

句型解析：
{parse_block}

文法：
{gram_block}

核心單字：{kw_block}
"""
    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    return fname

CARDS = [
("M24-001","Q",
"¿Por qué insiste el director / en revisar / las políticas de privacidad / si los usuarios ya confían / en la seguridad / de nuestra plataforma digital?",
"如果用戶們已經「信任」我們數位平台的安全性，主管為什麼還「堅持要」修改隱私政策？",
"Insistir en / Confiar en",
[
"【主要子句】¿Por qué insiste el director en revisar...（為什麼主管堅持要修改...）疑問句語序，動詞 insiste 先於主詞 el director，此為西文疑問句的正常倒裝語序。",
"【條件從句】si los usuarios ya confían en la seguridad...（如果用戶們已經信任安全性...）由 si 引導現實條件從句，與主句形成「既然...為何還...」的對比修辭語氣。",
"【介系詞片語】en revisar las políticas de privacidad — insistir en + 不定詞的固定搭配，表示堅持做某事，en 不可省略。",
"【介系詞片語】en la seguridad de nuestra plataforma digital — confiar en 的搭配受詞，表示信任某事物，de 引導後置限定語。",
"【名詞片語】nuestra plataforma digital — 物主形容詞 nuestra 修飾中心名詞 plataforma，形容詞 digital 後置修飾。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— insistir en：動詞 insistir 後必須搭配介系詞 en，再接不定詞或名詞，不可省略介系詞。例：Insiste en venir（他堅持要來）。",
"Régimen preposicional（動詞固定介系詞搭配）— confiar en：動詞 confiar 後接介系詞 en，表示信任某人或某事物。例：Confío en ti（我信任你）。",
"Inversión en interrogativas（疑問句倒裝語序）：¿Por qué + 動詞 + 主詞，西文疑問句中動詞先於主詞為正常語序，與中文語序不同。",
"Oración condicional con si（si 條件從句）：si + 直述式現在時，表示現實條件假設，形成修辭上的對比質疑語氣，與主句構成邏輯張力。",
],
["director","revisar","políticas","privacidad","usuarios","confiar","seguridad"],
),

("M24-002","A",
"Insiste en ello porque se ha enterado de que varias empresas de la competencia sufren por filtraciones de datos muy graves en Guayaquil.",
"他「堅持這樣做」是因為他「獲悉」有幾家競爭對手公司在瓜亞基爾「正遭受」非常嚴重的數據洩漏「所帶來的痛苦」。",
"Enterarse de / Sufrir por",
[
"【主要子句】Insiste en ello porque...（他堅持這樣做，因為...）主句以代詞 ello 代替前文提及的行動，porque 引導原因從句。",
"【原因從句】porque se ha enterado de que...（因為他獲悉...）se ha enterado 為現在完成時，強調剛剛得知的結果，de que 引導名詞子句作受詞。",
"【名詞子句】que varias empresas de la competencia sufren por filtraciones...（幾家競爭對手正遭受洩漏...）作 enterarse de 的受詞，描述所獲悉的具體內容。",
"【介系詞片語】por filtraciones de datos muy graves（因非常嚴重的數據洩漏）— sufrir por 表示因某事物而受苦，por 引導原因。",
"【地點狀語】en Guayaquil — 介系詞 en 引導地點狀語，修飾動詞 sufren，指明事件發生地點。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— enterarse de：動詞 enterarse 後必須接介系詞 de，再接名詞或 que 引導的子句，表示獲悉某事。例：Me enteré de la noticia（我獲悉了那則消息）。",
"Régimen preposicional（動詞固定介系詞搭配）— sufrir por：動詞 sufrir 後接介系詞 por，表示因某事物或某人而遭受痛苦。例：Sufre por su enfermedad（他因病痛而受苦）。",
"Pretérito perfecto compuesto（現在完成時）：se ha enterado 表示過去發生且對現在有影響的動作，強調「剛剛獲悉」的結果狀態，比簡單過去時更具時間關聯性。",
"Pronombre anafórico（照應代詞）— ello：中性代詞 ello 用於指代前文提及的整個行動或概念，不能用 lo 或 él 替代，保持語篇連貫。",
],
["insistir","enterarse","empresas","competencia","sufrir","filtraciones","datos"],
),

("M24-003","R",
"Me parece muy prudente; no podemos arriesgarnos a perder la credibilidad de los clientes por olvidarnos de actualizar los protocolos de encriptación.",
"我覺得這非常謹慎；我們不能因為「忘記」更新加密協議，而「冒著」失去客戶信任「的風險」。",
"Arriesgarse a / Olvidarse de",
[
"【評價句】Me parece muy prudente（我覺得這非常謹慎）— 動詞 parecer 以間接受詞 me 表示主觀評價，省略了受詞 eso，為口語中常見的結構。",
"【主要子句】no podemos arriesgarnos a perder la credibilidad...（我們不能冒著失去信任的風險）— 情態動詞 poder 否定式接反身動詞 arriesgarse a + 不定詞。",
"【原因狀語】por olvidarnos de actualizar los protocolos...（因為忘記更新協議）— por + 不定詞表示動作的原因，olvidarse de 固定搭配接不定詞。",
"【介系詞片語】a perder la credibilidad de los clientes — arriesgarse a + 不定詞的固定搭配，表示冒著做某事的風險。",
"【名詞片語】los protocolos de encriptación — 中心名詞 protocolos 加後置限定語 de encriptación，指加密協議。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— arriesgarse a：反身動詞 arriesgarse 後接介系詞 a，再接不定詞，表示冒著做某事的風險。例：Se arriesga a perderlo todo（他冒著失去一切的風險）。",
"Régimen preposicional（動詞固定介系詞搭配）— olvidarse de：反身動詞 olvidarse 後接介系詞 de，再接名詞或不定詞，表示忘記某事或忘記做某事。例：Me olvidé de llamarle（我忘了打電話給他）。",
"Por + infinitivo（por + 不定詞表原因）：por olvidarnos 表示「因為忘記」，此結構說明前面動作的原因，相當於 porque nos olvidamos。",
"Verbo modal negativo（情態動詞否定）：no podemos + 不定詞，表示「我們不能做某事」，強調禁止或不可能，podemos 為一人稱複數表示說話者包含在內。",
],
["parecer","arriesgarse","perder","credibilidad","clientes","olvidarse","actualizar","protocolos","encriptación"],
),

("M24-004","D",
"El experto advierte de que muchos jóvenes carecen de las herramientas necesarias para proteger su identidad digital frente a los algoritmos invasivos.",
"專家「警告（指出）」許多客戶「缺乏」保護自身數位身份、以應對侵入式演算法所需的必要工具。",
"Advertir de / Carecer de",
[
"【主要子句】El experto advierte de que...（專家警告指出...）— advertir de 固定搭配引導名詞子句，主詞為 el experto，動詞為現在時表示一般陳述。",
"【名詞子句】que muchos jóvenes carecen de las herramientas necesarias...（許多年輕人缺乏必要工具...）— 作 advertir de 的受詞，陳述警告的具體內容。",
"【介系詞片語】de las herramientas necesarias — carecer de 的固定搭配受詞，de 引導所缺乏的事物。",
"【目的不定詞片語】para proteger su identidad digital（為了保護其數位身份）— para + 不定詞表示目的，修飾 herramientas。",
"【對照介系詞片語】frente a los algoritmos invasivos（以應對侵入式演算法）— frente a 表示對抗或面對，指明保護的對象。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— advertir de：動詞 advertir 後接介系詞 de，引導名詞或 que 子句，表示警告或指出某事。例：Te advierto de que hay peligro（我警告你有危險）。",
"Régimen preposicional（動詞固定介系詞搭配）— carecer de：動詞 carecer 後必須接介系詞 de，表示缺乏某物，為非反身動詞，不能省略 de。例：Carecemos de recursos（我們缺乏資源）。",
"Para + infinitivo（para + 不定詞表目的）：para proteger 表示「為了保護」，說明 herramientas 的用途，此結構連接工具與其使用目的。",
"Frente a（對照介系詞片語）：frente a + 名詞表示「面對、應對、對抗」某事物，強調主動應對的姿態，常用於描述挑戰或威脅場景。",
],
["experto","advertir","jóvenes","carecer","herramientas","proteger","identidad","algoritmos"],
),

("M24-005","Q",
"¿Usted se opone a que la empresa utilice cookies de seguimiento para enterarse de cuáles son las preferencias de compra reales de los usuarios?",
"您「反對」公司使用追蹤 Cookie 來「獲悉（了解）」用戶們真實的購買偏好嗎？",
"Oponerse a / Enterarse de",
[
"【主要子句】¿Usted se opone a que...?（您反對...嗎？）— oponerse a 固定搭配，後接 que 引導虛擬式子句，表示反對某件事。",
"【名詞子句（虛擬式）】que la empresa utilice cookies de seguimiento（公司使用追蹤 Cookie）— utilice 為虛擬式現在時，由 oponerse a 觸發，表示說話者反對的行動。",
"【目的不定詞片語】para enterarse de cuáles son las preferencias...（為了獲悉哪些是偏好...）— para + 不定詞表目的，enterarse de 後接間接疑問句。",
"【間接疑問句】cuáles son las preferencias de compra reales de los usuarios（用戶們真實的購買偏好是哪些）— cuáles 引導間接疑問，語序為陳述句語序，非倒裝。",
"【名詞片語】las preferencias de compra reales de los usuarios — 多層後置修飾：de compra 限定偏好類型，reales 為形容詞修飾語，de los usuarios 指明所有者。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— oponerse a：反身動詞 oponerse 後接介系詞 a，可接名詞、不定詞或 que + 虛擬式，表示反對。例：Me opongo a esta decisión（我反對這個決定）。",
"Subjuntivo tras verbos de oposición（反對動詞後接虛擬式）：oponerse a + que 後必須使用虛擬式，因為表達的是說話者的意志或反對態度，而非客觀事實。",
"Interrogativa indirecta（間接疑問句）：cuáles son las preferencias 為間接疑問句，嵌入主句中作 enterarse de 的受詞，語序使用陳述句語序，不同於直接疑問句的倒裝。",
"Enterarse de + interrogativa indirecta（enterarse de 接間接疑問）：enterarse de 後可接 que 子句或間接疑問句，表示獲悉某具體信息的內容。",
],
["oponerse","empresa","utilizar","cookies","seguimiento","enterarse","preferencias","usuarios"],
),

("M24-006","A",
"Sí, me niego a aceptar cualquier práctica que atente contra el derecho a la intimidad de las personas sin su consentimiento explícito y firmado.",
"是的，我「拒絕」接受任何在未經人們明確且簽署同意的情況下、「侵犯」其隱私權的行為。",
"Negarse a / Atentar contra",
[
"【主要子句】me niego a aceptar cualquier práctica（我拒絕接受任何行為）— negarse a 固定搭配，後接不定詞，me 為反身代詞。",
"【關係從句（虛擬式）】que atente contra el derecho a la intimidad...（侵犯隱私權的...）— atente 為虛擬式現在時，因先行詞 cualquier práctica 為不確定泛指，觸發虛擬式。",
"【介系詞片語】contra el derecho a la intimidad de las personas — atentar contra 固定搭配，contra 表示侵犯的對象，a la intimidad 為 derecho 的後置限定語。",
"【條件狀語】sin su consentimiento explícito y firmado（在未經明確且簽署同意的情況下）— sin + 名詞片語表示缺少某條件，修飾整個行為。",
"【名詞片語】su consentimiento explícito y firmado — 物主形容詞 su 加中心名詞 consentimiento，兩個形容詞 explícito 和 firmado 以 y 連接，共同後置修飾。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— negarse a：反身動詞 negarse 後接介系詞 a，再接不定詞，表示拒絕做某事。例：Se niega a hablar（他拒絕說話）。",
"Régimen preposicional（動詞固定介系詞搭配）— atentar contra：動詞 atentar 後接介系詞 contra，表示侵犯或攻擊某事物，常用於正式或法律語境。",
"Subjuntivo en relativas con antecedente indefinido（不定先行詞後關係從句用虛擬式）：cualquier práctica 為不確定泛指的先行詞，其後的關係從句須使用虛擬式 atente，而非直述式。",
"Sin + sustantivo（sin + 名詞表條件缺失）：sin su consentimiento 表示「在沒有同意的情況下」，構成否定條件狀語，強調缺少必要前提。",
],
["negarse","aceptar","práctica","atentar","derecho","intimidad","personas","consentimiento"],
),

("M24-007","R",
"¡Totalmente de acuerdo! Las corporaciones deben preocuparse por la ética digital en lugar de centrarse únicamente en maximizar sus beneficios económicos.",
"完全同意！企業應該「擔心（重視）」數位倫理，而不是只「專注於」將其經濟利益最大化。",
"Preocuparse por / Centrarse en",
[
"【感嘆語】¡Totalmente de acuerdo!（完全同意！）— 省略主詞和動詞的慣用感嘆表達，等同於 Estoy totalmente de acuerdo，用於口語表示強烈贊同。",
"【主要子句】Las corporaciones deben preocuparse por la ética digital（企業應該重視數位倫理）— 情態動詞 deben 表義務，preocuparse por 固定搭配接名詞。",
"【對比狀語】en lugar de centrarse únicamente en maximizar...（而不是只專注於最大化...）— en lugar de + 不定詞表示「而非做某事」，形成對比。",
"【介系詞片語】por la ética digital — preocuparse por 固定搭配，表示關心或擔憂某事物。",
"【介系詞片語】en maximizar sus beneficios económicos — centrarse en + 不定詞，表示專注於做某事，únicamente 強調排他性。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— preocuparse por：反身動詞 preocuparse 後接介系詞 por，表示為某事擔憂或關心某事。例：Me preocupo por tu salud（我擔心你的健康）。",
"Régimen preposicional（動詞固定介系詞搭配）— centrarse en：反身動詞 centrarse 後接介系詞 en，再接名詞或不定詞，表示專注於某事。例：Me centro en el trabajo（我專注於工作）。",
"En lugar de + infinitivo（en lugar de + 不定詞表對比）：en lugar de centrarse 表示「而不是專注」，引導對比狀語，說明應避免的行為，與 en vez de 同義。",
"Deber + infinitivo（deber + 不定詞表義務）：deben preocuparse 表示「應該重視」，deber 為情態動詞，後接原形動詞，表示道德或邏輯上的義務。",
],
["corporaciones","preocuparse","ética","centrarse","maximizar","beneficios"],
),

("M24-008","D",
"Si los usuarios dependieran de las redes sociales para informarse, no tardarían en caer en campañas de desinformación diseñadas para manipular la opinión.",
"如果用戶們「依賴」社交媒體來獲取資訊，他們不用多久「就會（遲早）」陷入旨在操縱輿論的虛假訊息攻勢中。",
"Depender de / Tardar en",
[
"【條件從句（虛擬式過去）】Si los usuarios dependieran de las redes sociales...（如果用戶依賴社交媒體...）— si + 虛擬式過去時，表示與現實相反或假設性條件。",
"【主要子句（條件式）】no tardarían en caer en campañas...（他們不用多久就會陷入...）— 條件式 tardarían 呼應 si 從句，no tardar en 表示「很快就會」。",
"【介系詞片語（目的）】para informarse（為了獲取資訊）— para + 不定詞表目的，說明依賴社交媒體的用途。",
"【介系詞片語】en campañas de desinformación（陷入虛假訊息攻勢）— caer en 固定搭配，表示陷入某種不良狀態。",
"【後置分詞短語】diseñadas para manipular la opinión（旨在操縱輿論）— 過去分詞 diseñadas 修飾 campañas，para + 不定詞說明其設計目的。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— depender de：動詞 depender 後接介系詞 de，表示依賴或取決於某事物。例：Dependo de ti（我依賴你）。",
"Régimen preposicional（動詞固定介系詞搭配）— tardar en：動詞 tardar 後接介系詞 en，再接不定詞，表示花時間做某事，no tardar en 則表示「很快就...」。",
"Condicional irreal de presente（現在非現實條件句）：si + 虛擬式過去時（dependieran）+ 條件式（tardarían），表示與當前現實相反的假設，暗示用戶實際上不完全依賴社交媒體。",
"Participio en función adjetiva（形容詞性過去分詞）：diseñadas 為 diseñar 的過去分詞，作形容詞修飾 campañas，性數與所修飾名詞一致（陰性複數）。",
],
["usuarios","depender","redes","informarse","tardar","caer","campañas","desinformación","manipular"],
),

("M24-009","Q",
"¿A quién recurrió el gerente de marketing cuando se enteró de que la cuenta oficial de la compañía había sido hackeada por un grupo anónimo?",
"當行銷經理「獲悉」公司的官方帳號「被」一個匿名團體駭入時，他向誰「求助」？",
"Recurrir a / Enterarse de",
[
"【主要子句（疑問）】¿A quién recurrió el gerente de marketing...?（行銷經理向誰求助？）— a quién 為疑問詞組，recurrir a 固定搭配，recurrió 為簡單過去時。",
"【時間從句】cuando se enteró de que...（當他獲悉...時）— cuando 引導時間從句，enterarse de 後接 que 子句，動詞為簡單過去時。",
"【名詞子句】que la cuenta oficial de la compañía había sido hackeada...（公司官方帳號被駭入）— había sido hackeada 為過去完成時被動語態，表示獲悉時間點之前已發生的事。",
"【被動結構】había sido hackeada por un grupo anónimo — ser + 過去分詞構成被動態，por 引導動作執行者。",
"【名詞片語】el gerente de marketing — de marketing 為後置限定語，指明經理的職能領域。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— recurrir a：動詞 recurrir 後接介系詞 a，表示向某人或某機構求助、訴諸某方法。例：Recurrí a un abogado（我求助於一位律師）。",
"Voz pasiva（被動語態）：había sido hackeada = haber（過去完成時）+ sido + 過去分詞，三重結構構成過去完成時被動，表示在參照過去時間點之前已完成的被動動作。",
"Pluscuamperfecto（過去完成時）：había sido hackeada 表示在 se enteró（獲悉）這一過去動作發生之前，帳號已被駭，體現動作的先後時間順序。",
"Interrogativa con preposición antepuesta（介系詞前置疑問句）：a quién 中介系詞 a 前置於疑問詞前，這是西文疑問句的規範寫法，不可將介系詞置於句尾。",
],
["recurrir","gerente","marketing","enterarse","cuenta","compañía","hackear","grupo"],
),

("M24-010","A",
"Recurrió a una agencia especializada en ciberseguridad, la cual se encargó de restablecer el control y de informar a los seguidores sobre el incidente.",
"他「求助於」一家專門從事網路安全的機構，該機構「負責」恢復控制權並向粉絲們「通知」該事件的狀況。",
"Recurrir a / Encargarse de",
[
"【主要子句】Recurrió a una agencia especializada en ciberseguridad（他求助於一家專門網路安全的機構）— recurrir a 固定搭配，動詞為簡單過去時。",
"【後置形容詞分詞短語】especializada en ciberseguridad（專門從事網路安全的）— 過去分詞 especializada 作後置形容詞修飾 agencia，en 為固定搭配介系詞。",
"【關係從句】la cual se encargó de restablecer el control...（該機構負責恢復控制...）— la cual 為關係代詞，指代 agencia，se encargó de 固定搭配後接不定詞。",
"【並列不定詞片語】de restablecer el control y de informar a los seguidores sobre el incidente — 兩個 de + 不定詞並列，共同作 encargarse de 的受詞。",
"【介系詞片語】sobre el incidente — 介系詞 sobre 表示「關於」，引導 informar 的話題受詞。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— encargarse de：反身動詞 encargarse 後接介系詞 de，再接名詞或不定詞，表示負責做某事。例：Me encargo de la reunión（我負責這次會議）。",
"Pronombre relativo la cual（關係代詞 la cual）：la cual 可替換 que，用於有逗號隔開的非限定性關係從句，指代前面的 agencia，性數一致（陰性單數）。",
"Especializado en（形容詞固定搭配）：especializado/a en 表示「專門從事...」，由過去分詞轉化為形容詞，後接介系詞 en，此搭配廣泛用於描述機構或人員的專業領域。",
"Coordinación de infinitivos con preposición（介系詞與不定詞的並列）：de restablecer...y de informar，介系詞 de 在並列結構中重複使用，強調兩個動作均為 encargarse 的受詞，語義更清晰。",
],
["recurrir","agencia","ciberseguridad","encargarse","restablecer","control","informar","seguidores","incidente"],
),

("M24-011","Q",
"¿Cree usted que el éxito de una campaña en redes depende de la cantidad de datos personales que la empresa logre recopilar de sus clientes?",
"您認為一場社群媒體行銷的成功，「取決於」公司「成功」收集到多少客戶的個人數據嗎？",
"Depender de",
[
"【主要子句（疑問）】¿Cree usted que...?（您認為...嗎？）— creer 接 que 引導名詞子句，疑問句語序動詞 cree 先於主詞 usted。",
"【名詞子句】que el éxito de una campaña en redes depende de la cantidad...（行銷成功取決於數量...）— depende de 固定搭配，作 creer 的受詞。",
"【介系詞片語】de la cantidad de datos personales（取決於個人數據的數量）— depender de 的受詞，量詞結構 la cantidad de 後接被量化的名詞。",
"【關係從句（虛擬式）】que la empresa logre recopilar de sus clientes（公司成功收集到的）— logre 為虛擬式現在時，因先行詞 la cantidad 為不確定數量而使用虛擬式。",
"【動詞片語】logre recopilar — lograr + 不定詞表示「成功做到某事」，強調達成的結果。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— depender de：動詞 depender 後接介系詞 de，表示依賴或取決於某事物，不可與其他介系詞混用。",
"Subjuntivo en relativas con antecedente indefinido（不定先行詞後關係從句用虛擬式）：la cantidad que la empresa logre 中，logre 為虛擬式，因先行詞 la cantidad 指數量尚不確定，非特指已知數量。",
"Lograr + infinitivo（lograr + 不定詞）：lograr 後接原形動詞，表示「成功做到...」，強調達成某目標的結果，含有積極成就的語義。",
"Cantidad de（量詞結構）：la cantidad de + 名詞為常見量詞結構，後面的 que 引導關係從句修飾 cantidad，說明數量的性質或來源。",
],
["éxito","campaña","redes","depender","cantidad","datos","empresa","lograr","recopilar","clientes"],
),

("M24-012","A",
"No del todo; depende más de la creatividad del mensaje, aunque reconozco que segmentar el público contribuye a mejorar el impacto de la publicidad.",
"不完全是；更「取決於」訊息的創意，儘管我承認對受眾進行細分「有助於」改善廣告的衝擊力。",
"Depender de / Contribuir a",
[
"【否定片語】No del todo（不完全是）— 慣用否定表達，修飾前文的問題，del todo 表示「完全、全部」，加 no 構成部分否定。",
"【主要子句】depende más de la creatividad del mensaje（更取決於訊息的創意）— 省略主詞（承接前文語境），depender de 固定搭配，más 表示程度比較。",
"【讓步從句】aunque reconozco que...（儘管我承認...）— aunque 引導讓步從句，reconocer que 後接直述式子句，表示承認客觀事實。",
"【名詞子句】que segmentar el público contribuye a mejorar el impacto...（細分受眾有助於改善影響力）— contribuir a 固定搭配，後接不定詞。",
"【介系詞片語】a mejorar el impacto de la publicidad — contribuir a + 不定詞，表示有助於做某事，de la publicidad 為後置限定語。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— contribuir a：動詞 contribuir 後接介系詞 a，再接名詞或不定詞，表示有助於或貢獻於某事。例：Contribuye a mejorar la situación（有助於改善情況）。",
"Aunque + indicativo vs. subjuntivo（aunque 讓步從句的語式選擇）：aunque reconozco 使用直述式，表示說話者承認的客觀事實；若使用虛擬式則表示假設或不確定情況。",
"No del todo（部分否定慣用語）：no del todo 表示「不完全、並非全然」，屬於程度否定，不等同於完全否定 no，是口語中常用的委婉表達。",
"Infinitivo en función de sujeto（不定詞作主詞）：segmentar el público 為不定詞片語，作動詞 contribuye 的主詞，西文中不定詞可作主詞，此時動詞用第三人稱單數。",
],
["depender","creatividad","mensaje","reconocer","segmentar","público","contribuir","mejorar","impacto","publicidad"],
),

("M24-013","R",
"¡Es un dilema! Me preocupa que, por obsesionarse con las métricas, muchas marcas terminen por violar los límites de la privacidad de los consumidores.",
"真是個兩難！我「擔心」許多品牌因為「痴迷於」數據指標，最終「落得」侵犯消費者隱私邊界「的下場」。",
"Obsesionarse con / Terminar por",
[
"【感嘆語】¡Es un dilema!（真是個兩難！）— 簡單陳述句作感嘆，直接表達說話者對情況的判斷。",
"【主要子句】Me preocupa que...（我擔心...）— 無人稱結構，動詞 preocupar 以間接受詞 me 表示受影響者，que 後接虛擬式子句，表示說話者的擔憂。",
"【原因狀語】por obsesionarse con las métricas（因為痴迷於數據指標）— por + 不定詞表原因，obsesionarse con 固定搭配。",
"【名詞子句（虛擬式）】que muchas marcas terminen por violar los límites...（許多品牌最終侵犯邊界）— terminen 為虛擬式，受 me preocupa 觸發，terminar por + 不定詞表示最終做了某事。",
"【介系詞片語】de la privacidad de los consumidores — 雙重後置限定語，de la privacidad 限定 límites 的性質，de los consumidores 指明所屬。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— obsesionarse con：反身動詞 obsesionarse 後接介系詞 con，表示對某事物痴迷或過度執著。例：Se obsesiona con el trabajo（他對工作痴迷）。",
"Terminar por + infinitivo（terminar por + 不定詞）：表示「最終做了某事」，帶有結果往往出乎意料或令人遺憾的語義色彩。例：Terminó por rendirse（他最終放棄了）。",
"Verbos de emoción con subjuntivo（情感動詞後接虛擬式）：preocupar 表示情感反應，後接 que 子句須使用虛擬式（terminen），因為表達的是說話者的主觀情感，而非客觀事實陳述。",
"Por + infinitivo（por + 不定詞表原因）：por obsesionarse 表示「因為痴迷」，此結構說明後文動作的原因，相當於 porque se obsesionan，但更簡潔。",
],
["dilema","preocupar","obsesionarse","métricas","marcas","terminar","violar","límites","privacidad","consumidores"],
),

("M24-014","D",
"El director general se comprometió a no vender la base de datos a terceros, insistiendo en que la confianza del cliente está por encima de todo.",
"總經理「承諾」絕不將資料庫賣給第三方，並「堅持認為」客戶的信任「高於」一切。",
"Comprometerse a / Insistir en",
[
"【主要子句】El director general se comprometió a no vender la base de datos a terceros（總經理承諾不將資料庫賣給第三方）— comprometerse a 固定搭配接不定詞，no 否定不定詞。",
"【伴隨狀語（現在分詞）】insistiendo en que...（並堅持認為...）— 現在分詞 insistiendo 引導伴隨狀語，說明承諾時同時表達的態度，insistir en 後接 que 子句。",
"【名詞子句】que la confianza del cliente está por encima de todo（客戶的信任高於一切）— 使用直述式，因 insistir en 此處表示主張客觀事實而非意志。",
"【慣用語】por encima de todo（高於一切）— 介系詞片語 por encima de 表示「在...之上、超越」，todo 為泛指代詞。",
"【間接受詞】a terceros — 介系詞 a 引導售賣的對象，terceros 為名詞，指第三方。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— comprometerse a：反身動詞 comprometerse 後接介系詞 a，再接不定詞，表示承諾做某事。例：Me comprometo a cumplirlo（我承諾履行）。",
"Insistir en + que（insistir en 接 que 子句）：insistir en + que 後接直述式時表示堅持某一客觀主張；後接虛擬式時表示堅持要求某人做某事，語式選擇取決於語義。",
"Negación del infinitivo（不定詞的否定）：no vender，以 no 置於不定詞前構成否定不定詞，用於否定承諾、禁止等情境。",
"Gerundio en función adverbial（副詞性現在分詞）：insistiendo 作伴隨狀語，描述主要動作（comprometerse）發生時同時進行的附帶動作或態度，現在分詞主詞須與主句主詞相同。",
],
["director","comprometerse","vender","base","datos","terceros","insistir","confianza","cliente"],
),

("M24-015","Q",
"¿Por qué te sorprendes de que el gobierno intente regular las plataformas si estas se niegan a colaborar en la lucha contra el cibercrimen?",
"如果這些平台「拒絕」在打擊網路犯罪中進行合作，你為什麼還對政府「試圖」管制它們感到「驚訝」？",
"Sorprenderse de / Negarse a",
[
"【主要子句（疑問）】¿Por qué te sorprendes de que el gobierno intente regular las plataformas...?（你為什麼對政府試圖管制平台感到驚訝？）— sorprenderse de + que 虛擬式固定結構。",
"【名詞子句（虛擬式）】que el gobierno intente regular las plataformas（政府試圖管制平台）— intente 為虛擬式，受情感動詞 sorprenderse de 觸發。",
"【條件從句】si estas se niegan a colaborar en la lucha...（如果這些平台拒絕合作...）— si + 直述式表示現實條件，estas 指代前文的 plataformas。",
"【介系詞片語】a colaborar en la lucha contra el cibercrimen — negarse a + 不定詞，en la lucha 為地點兼抽象場域，contra 表示對抗。",
"【名詞片語】la lucha contra el cibercrimen — 名詞 lucha 加後置介系詞片語 contra el cibercrimen，構成「打擊網路犯罪」。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— sorprenderse de：反身動詞 sorprenderse 後接介系詞 de，引導名詞或 que 子句，表示對某事感到驚訝。例：Me sorprendo de su respuesta（我對他的回答感到驚訝）。",
"Régimen preposicional（動詞固定介系詞搭配）— negarse a：反身動詞 negarse 後接介系詞 a，再接不定詞，表示拒絕做某事。",
"Subjuntivo tras verbos de emoción（情感動詞後接虛擬式）：sorprenderse de + que 後須使用虛擬式（intente），因為表達說話者主觀情感反應，而非陳述客觀事實。",
"Pronombre demostrativo estas（指示代詞 estas）：estas 指代前文出現的 las plataformas，性數一致（陰性複數），起語篇銜接功能，避免重複名詞。",
],
["sorprenderse","gobierno","intentar","regular","plataformas","negarse","colaborar","lucha","cibercrimen"],
),

("M24-016","A",
"Me sorprendo de la falta de diálogo; si ambas partes se dedicaran a buscar un consenso, la privacidad del ciudadano saldría muy beneficiada.",
"我對缺乏對話感到「驚訝」；如果雙方都能「致力於」尋求共識，公民的隱私將會「大為」受益。",
"Sorprenderse de / Dedicarse a",
[
"【主要子句】Me sorprendo de la falta de diálogo（我對缺乏對話感到驚訝）— sorprenderse de 固定搭配，de 後接名詞 la falta de diálogo。",
"【條件從句（虛擬式過去）】si ambas partes se dedicaran a buscar un consenso（如果雙方都致力於尋求共識）— si + 虛擬式過去時，表示假設性或反現實條件。",
"【主句（條件式）】la privacidad del ciudadano saldría muy beneficiada（公民隱私將會大為受益）— 條件式 saldría 與 si 從句構成假設性條件句，salir + 形容詞表示「以...狀態出現」。",
"【介系詞片語】a buscar un consenso — dedicarse a + 不定詞，表示致力於做某事。",
"【修飾語】muy beneficiada — 副詞 muy 修飾過去分詞形容詞 beneficiada，說明受益的程度。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— dedicarse a：反身動詞 dedicarse 後接介系詞 a，再接名詞或不定詞，表示致力於、從事某事。例：Se dedica a la investigación（他致力於研究）。",
"Condicional irreal de presente（現在非現實條件句）：si + 虛擬式過去時（dedicaran）+ 條件式（saldría），表示假設性情況，暗示雙方目前實際上並未致力於尋求共識。",
"Salir + adjetivo（salir + 形容詞）：salir beneficiada 表示「以受益的狀態出現」，salir 作連繫動詞接形容詞，描述主詞達到的狀態結果，類似 quedar 的用法。",
"Ambas partes（雙方）：ambas 為形容詞，表示「兩者都、雙方」，性數與所修飾名詞一致，強調兩方均需參與的必要性。",
],
["sorprenderse","falta","diálogo","dedicarse","buscar","consenso","privacidad","ciudadano"],
),

("M24-017","R",
"Tienes razón; es hora de que las grandes tecnológicas dejen de actuar de forma unilateral y empiecen a respetar las leyes locales de cada país。",
"你說得對；大型科技公司是時候「停止」單方面行事，並「開始」尊重每個國家的當地法律了。",
"Dejar de / Empezar a",
[
"【慣用語】Tienes razón（你說得對）— 固定短語，字面義為「你有道理」，tener razón 表示「正確、有道理」，用於表示同意對方的觀點。",
"【主要子句】es hora de que...（是時候...了）— 非人稱結構 es hora de que + 虛擬式，表示某事到了應該發生的時候。",
"【名詞子句（虛擬式）】que las grandes tecnológicas dejen de actuar...y empiecen a respetar...（大型科技公司停止...並開始...）— dejen 和 empiecen 均為虛擬式，並列兩個動作。",
"【介系詞片語（方式）】de forma unilateral（以單方面方式）— de forma + 形容詞為副詞性片語，修飾動詞 actuar，表示行動的方式。",
"【名詞片語】las leyes locales de cada país — 中心名詞 leyes 加形容詞 locales 及後置限定語 de cada país。",
],[
"Dejar de + infinitivo（dejar de + 不定詞）：表示「停止做某事」，動作中斷，dejar de 為固定搭配，不定詞說明被中斷的動作。例：Dejó de fumar（他戒菸了）。",
"Empezar a + infinitivo（empezar a + 不定詞）：表示「開始做某事」，動作起始，empezar a 為固定搭配，與 dejar de 形成起止對比。例：Empieza a llover（開始下雨）。",
"Es hora de que + subjuntivo（是時候...的虛擬式結構）：es hora de que 後必須使用虛擬式，因為表達的是說話者的期望或判斷，而非描述現實情況。",
"Coordinación de verbos en subjuntivo（虛擬式動詞的並列）：dejen de actuar...y empiecen a respetar，兩個虛擬式動詞以 y 並列，共同作 es hora de que 的子句謂語，表達期望的兩個並列行動。",
],
["tecnológicas","dejar","actuar","empezar","respetar","leyes","país"],
),

("M24-018","D",
"Si la aplicación careciera de un sistema de verificación en dos pasos, los usuarios se expondrían a que sus contraseñas fueran robadas con gran facilidad.",
"如果該 APP 「缺乏」兩步驟驗證系統，用戶們將會「面臨」其密碼極其容易「被」盜「的風險」。",
"Carecer de / Exponerse a",
[
"【條件從句（虛擬式過去）】Si la aplicación careciera de un sistema de verificación en dos pasos（如果 APP 缺乏兩步驟驗證系統）— si + 虛擬式過去時，表示假設性條件。",
"【主句（條件式）】los usuarios se expondrían a que...（用戶們將面臨...的風險）— 條件式 expondrían，exponerse a + que 子句，表示面臨某事的風險。",
"【名詞子句（虛擬式）】que sus contraseñas fueran robadas con gran facilidad（密碼被輕易盜取）— fueran robadas 為虛擬式過去時被動，受 exponerse a 觸發。",
"【介系詞片語】de un sistema de verificación en dos pasos — carecer de 的受詞，en dos pasos 為後置修飾語，指驗證步驟數。",
"【方式狀語】con gran facilidad（以極大的容易度）— con + 名詞片語作方式狀語，修飾被動動作 fueran robadas。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— carecer de：動詞 carecer 後必須接介系詞 de，表示缺乏某物，為非反身動詞。",
"Régimen preposicional（動詞固定介系詞搭配）— exponerse a：反身動詞 exponerse 後接介系詞 a，可接名詞或 que + 虛擬式，表示使自己面臨某風險或暴露於某情況。",
"Condicional irreal de presente（現在非現實條件句）：si + 虛擬式過去時（careciera）+ 條件式（expondrían），表示與現實相反的假設，即 APP 實際上有此驗證系統。",
"Voz pasiva con subjuntivo（虛擬式被動語態）：fueran robadas = ser 的虛擬式過去時（fueran）+ 過去分詞 robadas，構成被動語態，主詞 contraseñas 為被動受事者。",
],
["aplicación","carecer","verificación","usuarios","exponerse","contraseñas","robar"],
),

("M24-019","Q",
"¿De qué se quejan los usuarios cuando la red social cambia sus condiciones de servicio sin avisar a la comunidad con suficiente antelación?",
"當社交網路在沒有提前足夠時間「通知」社群的情況下「更改」其服務條款時，用戶們是在「抱怨」什麼？",
"Quejarse de / Avisar a",
[
"【主要子句（疑問）】¿De qué se quejan los usuarios...?（用戶們在抱怨什麼？）— de qué 為疑問詞組，介系詞 de 前置，quejarse de 固定搭配。",
"【時間從句】cuando la red social cambia sus condiciones de servicio（當社交網路更改服務條款時）— cuando 引導時間從句，cambia 為現在時，表示習慣性動作。",
"【方式狀語】sin avisar a la comunidad con suficiente antelación（在未提前足夠時間通知社群的情況下）— sin + 不定詞表示缺少某伴隨動作。",
"【名詞片語】sus condiciones de servicio — 物主形容詞 sus 加中心名詞 condiciones，de servicio 為後置限定語。",
"【介系詞片語】con suficiente antelación（以足夠的提前量）— con + 名詞作方式狀語，修飾 avisar，說明通知的時間充裕度。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— quejarse de：反身動詞 quejarse 後接介系詞 de，引導名詞或 que 子句，表示對某事抱怨。例：Se quejan de la calidad（他們抱怨品質）。",
"Interrogativa con preposición antepuesta（介系詞前置疑問句）：¿De qué? 中介系詞 de 置於疑問詞前，對應動詞 quejarse de 的搭配，西文規範要求介系詞不可懸置於句尾。",
"Sin + infinitivo（sin + 不定詞表缺少伴隨動作）：sin avisar 表示「在未通知的情況下」，否定伴隨條件，相當於 sin que avisaran，但主詞相同時用不定詞更簡潔。",
"Con + sustantivo（con + 名詞表方式）：con suficiente antelación 為方式狀語，con 引導名詞片語說明動作執行的條件或方式，此為西文中常見的副詞性結構。",
],
["quejarse","usuarios","red","social","cambiar","condiciones","servicio","avisar","comunidad"],
),

("M24-020","A",
"Se quejan de la falta de transparencia, argumentando que la empresa se aprovecha de la ambigüedad legal para comercializar sus fotos privadas.",
"他們「抱怨」缺乏透明度，並辯稱公司「利用（佔便宜）」法律的模糊性來將他們的私密照片商品化。",
"Quejarse de / Aprovecharse de",
[
"【主要子句】Se quejan de la falta de transparencia（他們抱怨缺乏透明度）— quejarse de 固定搭配，de 後接名詞 la falta de transparencia。",
"【伴隨狀語（現在分詞）】argumentando que...（並辯稱...）— 現在分詞 argumentando 引導伴隨狀語，描述抱怨時同時進行的辯述動作。",
"【名詞子句】que la empresa se aprovecha de la ambigüedad legal para comercializar...（公司利用法律模糊性商品化...）— 直述式，argumentar 表示客觀陳述主張。",
"【介系詞片語】de la ambigüedad legal — aprovecharse de 固定搭配的受詞，de 引導所利用的對象。",
"【目的不定詞片語】para comercializar sus fotos privadas（為了商品化他們的私密照片）— para + 不定詞表目的，說明利用的意圖。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— aprovecharse de：反身動詞 aprovecharse 後接介系詞 de，表示利用、佔...的便宜。例：Se aprovecha de tu bondad（他利用你的善良）。",
"Gerundio en función adverbial（副詞性現在分詞）：argumentando 作伴隨狀語，與主句動作 quejan 同時進行，現在分詞主詞與主句主詞相同（省略）。",
"Falta de + sustantivo（缺乏...的結構）：la falta de transparencia 表示「缺乏透明度」，falta de 為固定名詞結構，後接所缺乏的事物，常見於正式語境。",
"Para + infinitivo（para + 不定詞表目的）：para comercializar 說明行動的目的，暗示公司蓄意利用模糊性來達成商業目標，目的狀語修飾 aprovecharse de 整個動作。",
],
["quejarse","falta","transparencia","empresa","aprovecharse","ambigüedad","comercializar","fotos"],
),

("M24-021","Q",
"¿A qué se debe que tantas personas sigan subiendo fotos de sus hijos a internet a pesar de que los expertos advierten de los riesgos?",
"儘管專家們「警告（指出）」了風險，為什麼還是有這麼多人「持續上傳」孩子的照片到網路上，這究竟是「歸因於」什麼？",
"Deberse a / Advertir de",
[
"【主要子句（疑問）】¿A qué se debe que tantas personas sigan subiendo fotos...?（這歸因於什麼...？）— a qué 為疑問詞組，deberse a 固定搭配，que 後接虛擬式子句。",
"【名詞子句（虛擬式）】que tantas personas sigan subiendo fotos de sus hijos a internet（那麼多人持續上傳孩子照片）— sigan 為虛擬式現在時，受 deberse a 觸發，seguir + 現在分詞表持續進行。",
"【讓步從句】a pesar de que los expertos advierten de los riesgos（儘管專家警告了風險）— a pesar de que + 直述式，表示讓步，承認存在相反情況。",
"【介系詞片語】de los riesgos — advertir de 固定搭配的受詞，de 引導所警告的內容。",
"【名詞片語】fotos de sus hijos — 中心名詞 fotos 加後置限定語 de sus hijos，物主形容詞 sus 指代 personas。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— deberse a：反身動詞 deberse 後接介系詞 a，表示歸因於某事物。例：Se debe a un error（這是由於一個錯誤）。",
"Advertir de（advertir de 固定搭配）：advertir 後接介系詞 de，引導名詞或 que 子句，表示警告指出某事，de 不可省略。",
"Seguir + gerundio（seguir + 現在分詞表持續）：sigan subiendo 表示「持續上傳」，seguir 作半助動詞，後接現在分詞，強調動作的延續性。",
"A pesar de que + indicativo（a pesar de que 讓步從句）：a pesar de que 引導讓步從句，advierten 使用直述式，表示讓步的事實是客觀存在的現實。",
],
["deberse","personas","subir","fotos","hijos","internet","expertos","advertir","riesgos"],
),

("M24-022","A",
"Se debe a la necesidad de aprobación social; muchos padres no se dan cuenta de que están exponiendo a los menores a peligros digitales graves.",
"這「歸因於」社會認同的需求；許多父母沒有「意識到」自己正在讓未成年人「面臨」嚴重的數位危險。",
"Deberse a / Exponerse a",
[
"【主要子句】Se debe a la necesidad de aprobación social（這歸因於社會認同的需求）— deberse a 固定搭配，de aprobación social 為後置限定語。",
"【並列主句】muchos padres no se dan cuenta de que...（許多父母沒有意識到...）— darse cuenta de + que 固定搭配，否定式表示缺乏意識。",
"【名詞子句】que están exponiendo a los menores a peligros digitales graves（正在讓未成年人面臨嚴重數位危險）— 現在進行時，a los menores 為直接受詞，a peligros 為 exponer a 的受詞。",
"【雙重 a 結構】exponiendo a los menores a peligros — exponer 的雙重受詞結構：a los menores 為受詞（物），a peligros 為 exponer a 固定搭配的受詞。",
"【名詞片語】peligros digitales graves — 中心名詞 peligros 加兩個後置形容詞修飾，digitales 指類型，graves 指嚴重程度。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— darse cuenta de：固定搭配 darse cuenta de + que 子句，表示意識到某事。例：No me di cuenta de que era tarde（我沒意識到已經很晚了）。",
"Exponer a alguien a algo（exponer 的雙重受詞）：exponer 可接兩個介系詞 a，第一個引導受影響的人（los menores），第二個引導危險或風險（peligros），形成雙重 a 結構。",
"Estar + gerundio（進行時表當下持續）：están exponiendo 強調父母正在進行中的行為，而非過去或假設，暗示這是當前持續存在的問題。",
"Aprobación social（社會認同）：aprobación 名詞後加形容詞 social，social 後置修飾名詞，此為西文名詞片語的標準語序，形容詞通常後置。",
],
["deberse","necesidad","aprobación","padres","darse","cuenta","exponer","menores","peligros"],
),

("M24-023","R",
"¡Es alarmante! Es necesario que las escuelas contribuyan a educar a las familias sobre cómo protegerse de los depredadores en la red.",
"令人震驚！學校有必要「有助於」教育家庭關於如何「保護自己免受」網路上捕食者的侵害。",
"Contribuir a / Protegerse de",
[
"【感嘆語】¡Es alarmante!（令人震驚！）— 非人稱評價句，形容詞 alarmante 表示說話者的情緒反應，主詞為泛指的情況。",
"【主要子句】Es necesario que las escuelas contribuyan a educar...（學校有必要有助於教育...）— 非人稱表達 es necesario + que 虛擬式，表示必要性。",
"【名詞子句（虛擬式）】que las escuelas contribuyan a educar a las familias（學校有助於教育家庭）— contribuyan 為虛擬式，contribuir a + 不定詞固定搭配。",
"【介系詞片語（話題）】sobre cómo protegerse de los depredadores en la red（關於如何保護自己免受網路捕食者侵害）— sobre 引導話題，cómo + 不定詞為間接疑問式。",
"【介系詞片語】de los depredadores en la red — protegerse de 固定搭配，de 引導所防範的對象，en la red 為地點狀語。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— contribuir a：動詞 contribuir 後接介系詞 a，再接名詞或不定詞，表示有助於或貢獻。",
"Régimen preposicional（動詞固定介系詞搭配）— protegerse de：反身動詞 protegerse 後接介系詞 de，表示保護自己免受某事物侵害。例：Protégete del sol（保護自己免受太陽傷害）。",
"Es necesario que + subjuntivo（必要性句型）：es necesario que 後必須使用虛擬式（contribuyan），因為表達的是說話者的判斷和需求，而非描述現實。",
"Cómo + infinitivo（如何...的不定詞結構）：sobre cómo protegerse 中，cómo + 不定詞構成間接疑問式，嵌入介系詞片語，說明教育的具體內容。",
],
["escuelas","contribuir","educar","familias","protegerse","depredadores","red"],
),

("M24-024","D",
"El nuevo reglamento europeo obliga a todas las empresas a borrar los datos del usuario si este insiste en ejercer su derecho al olvido digital.",
"如果用戶「堅持」行使其數位遺忘權，新歐洲法規將「強制要求」所有公司刪除該用戶的數據。",
"Obligar a / Insistir en",
[
"【主要子句】El nuevo reglamento europeo obliga a todas las empresas a borrar los datos del usuario（新歐洲法規強制要求所有公司刪除用戶數據）— obligar a alguien a + 不定詞，雙重 a 結構。",
"【雙重 a 結構】obliga a todas las empresas a borrar — obligar 的結構：a todas las empresas 為受影響的對象（間接受詞），a borrar 為強制做的動作（不定詞）。",
"【條件從句】si este insiste en ejercer su derecho al olvido digital（如果用戶堅持行使數位遺忘權）— si + 直述式表現實條件，este 指代 el usuario。",
"【介系詞片語】en ejercer su derecho al olvido digital — insistir en + 不定詞固定搭配，al olvido digital 為 derecho 的後置限定語（al = a + el）。",
"【名詞片語】el derecho al olvido digital — 法律術語，derecho al + 名詞，指法律賦予的權利，al 為縮合介系詞。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— obligar a：動詞 obligar 後接介系詞 a，引導受影響的人；再接介系詞 a，引導被強制做的動作（不定詞），形成雙重 a 結構。例：Te obligo a estudiar（我強制你學習）。",
"Insistir en + infinitivo（insistir en + 不定詞）：表示堅持做某事，en 為固定介系詞，後接不定詞說明所堅持的動作。",
"Pronombre demostrativo este（指示代詞 este）：este 指代前文的 el usuario，為陽性單數，起語篇銜接作用，在正式書面語中常用以替代重複名詞。",
"Derecho a + sustantivo（derecho a 表示某種權利）：el derecho al olvido digital 為法律術語，derecho a 後接名詞表示某種具體的法律權利，al 為 a + el 的縮合形式。",
],
["reglamento","europeo","obligar","empresas","borrar","datos","usuario","insistir","ejercer","derecho","olvido"],
),

("M24-025","Q",
"¿Por qué te asustas de que las aplicaciones escuchen tus conversaciones si tú mismo aceptaste los términos al instalar el software?",
"如果你在「安裝」軟體時自己「接受了」條款，你為什麼還對應用程式「偷聽」你的對話感到「害怕」？",
"Asustarse de / Al + Infinitivo",
[
"【主要子句（疑問）】¿Por qué te asustas de que las aplicaciones escuchen tus conversaciones...?（你為什麼對應用程式偷聽你的對話感到害怕？）— asustarse de + que 虛擬式固定結構。",
"【名詞子句（虛擬式）】que las aplicaciones escuchen tus conversaciones（應用程式偷聽你的對話）— escuchen 為虛擬式現在時，受情感動詞 asustarse de 觸發。",
"【條件從句】si tú mismo aceptaste los términos（如果你自己接受了條款）— si + 直述式過去時，tú mismo 強調是說話對象自己的行為。",
"【時間狀語】al instalar el software（在安裝軟體時）— al + 不定詞表示動作同時或緊接發生的時間，等同於 cuando instalaste。",
"【強調語】tú mismo（你自己）— mismo 跟隨人稱代詞，強調主詞本身親自做了某事，語氣含輕微指責或反問。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— asustarse de：反身動詞 asustarse 後接介系詞 de，引導名詞或 que 子句，表示對某事感到害怕或受驚。例：Me asusto de las alturas（我對高度感到恐懼）。",
"Al + infinitivo（al + 不定詞表時間）：al instalar 表示「在安裝時」，al + 不定詞為時間狀語結構，表示兩個動作同時或緊接發生，主詞須與主句主詞相同。",
"Subjuntivo tras verbos de emoción（情感動詞後接虛擬式）：asustarse de + que 後須使用虛擬式（escuchen），因為表達說話者的主觀情感反應。",
"Mismo como intensificador（mismo 作加強語）：tú mismo 中 mismo 加強代詞語氣，強調「你自己親自」，帶有輕微的對比或指責語氣，暗示對方應負責任。",
],
["asustarse","aplicaciones","escuchar","conversaciones","aceptar","términos","instalar","software"],
),
]

count = 0
for entry in CARDS:
    old_id, ctype, es, zh, gram_title, parse_pts, gram_pts, keywords = entry
    new_id = convert_id(old_id)
    write_card(new_id, ctype, es, zh, gram_title, parse_pts, gram_pts, keywords)
    count += 1
    print(f"OK: {new_id}")

print(f"\nPart 1 done: {count} cards")

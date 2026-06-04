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

CARDS = [
("M24-026","A",
"Me asusto de que no haya un control real; nadie se detiene a leer esos contratos tan largos porque todos tenemos prisa por usar la tecnología.",
"我對缺乏真實管制感到「害怕」；沒有人會「停下來（特地）」去讀那些如此冗長的合約，因為我們大家都在趕著使用科技。",
"Asustarse de / Detenerse a",
[
"【主要子句】Me asusto de que no haya un control real（我對缺乏真實管制感到害怕）— asustarse de + que 虛擬式，haya 為 haber 的虛擬式現在時，表示存在與否的虛擬。",
"【並列主句】nadie se detiene a leer esos contratos tan largos（沒有人特地停下來讀那些冗長合約）— detenerse a + 不定詞，否定主詞 nadie 強調完全沒有人做此行為。",
"【原因從句】porque todos tenemos prisa por usar la tecnología（因為我們大家都趕著使用科技）— porque 引導原因從句，tener prisa por 固定搭配表示急於做某事。",
"【名詞片語】esos contratos tan largos — 指示形容詞 esos 加中心名詞 contratos，tan + 形容詞 largos 表示程度，「如此冗長的」。",
"【介系詞片語】por usar la tecnología — tener prisa por + 不定詞，表示急於做某事的固定搭配。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— asustarse de：反身動詞 asustarse 後接介系詞 de，引導名詞或 que 子句，表示對某事感到害怕。",
"Régimen preposicional（動詞固定介系詞搭配）— detenerse a：反身動詞 detenerse 後接介系詞 a，再接不定詞，表示特地停下來做某事，含有刻意暫停以執行某動作的語義。例：Se detuvo a pensar（他停下來思考）。",
"Nadie + verbo（否定代詞 nadie）：nadie 作主詞時，謂語動詞用第三人稱單數，強調完全沒有任何人，語氣比 ninguno 更絕對。",
"Tener prisa por + infinitivo（tener prisa por + 不定詞）：固定搭配，表示急於做某事，por 引導急於進行的動作，常見於口語表達倉促感。",
],
["asustarse","control","detenerse","leer","contratos","prisa","usar","tecnología"],
),

("M24-027","R",
"¡Ahí está el truco! Las empresas se basan en esa falta de tiempo de los consumidores para apoderarse de una cantidad ingente de datos privados.",
"竅門就在這裡！企業正是「基於」消費者缺乏時間這一點，來「霸佔（據為己有）」數量龐大的私密數據。",
"Basarse en / Apoderarse de",
[
"【感嘆語】¡Ahí está el truco!（竅門就在這裡！）— 慣用感嘆句，ahí 為地點副詞，estar 表示存在，truco 為口語詞「竅門、把戲」，強調說話者的頓悟。",
"【主要子句】Las empresas se basan en esa falta de tiempo de los consumidores（企業基於消費者缺乏時間這一點）— basarse en 固定搭配，en 後接名詞片語。",
"【目的不定詞片語】para apoderarse de una cantidad ingente de datos privados（為了霸佔大量私密數據）— para + 不定詞表目的，apoderarse de 固定搭配。",
"【介系詞片語】en esa falta de tiempo de los consumidores — basarse en 的受詞，esa 為指示形容詞指代前文提及的情況，雙重後置限定語說明缺乏的內容和所屬者。",
"【名詞片語】una cantidad ingente de datos privados — 量詞結構 cantidad de，ingente 為形容詞「龐大的」修飾 cantidad，de datos privados 為後置限定語。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— basarse en：反身動詞 basarse 後接介系詞 en，表示基於某事物、以某事物為依據。例：Me baso en los datos（我以數據為依據）。",
"Régimen preposicional（動詞固定介系詞搭配）— apoderarse de：反身動詞 apoderarse 後接介系詞 de，表示掌控、據為己有某事物。例：Se apoderó del territorio（他佔領了那片領土）。",
"Para + infinitivo（para + 不定詞表目的）：para apoderarse 說明企業利用消費者缺乏時間的最終目的，暗示蓄意的商業策略。",
"Cantidad ingente（大量的表達）：ingente 為正式形容詞，意為「龐大的、巨量的」，修飾 cantidad，比常見的 mucha 語氣更正式且強調數量之巨，常見於書面語境。",
],
["empresas","basarse","falta","tiempo","consumidores","apoderarse","cantidad","datos"],
),

("M24-028","D",
"Si el comité de seguridad no se hubiera encargado de encriptar los archivos confidenciales, hoy estaríamos sufriendo por una demanda millonaria de los clientes.",
"如果安全委員會當時沒「負責（過）」加密機密檔案，我們今天「就會正在遭受」因客戶提出數百萬美元訴訟「所帶來的痛苦」了。",
"Encargarse de / Sufrir por",
[
"【條件從句（虛擬式過去完成）】Si el comité de seguridad no se hubiera encargado de encriptar los archivos...（如果安全委員會當時沒負責加密檔案...）— si + 虛擬式過去完成時，表示與過去事實相反的假設。",
"【主句（條件式進行時）】hoy estaríamos sufriendo por una demanda millonaria...（我們今天就會正在遭受訴訟...）— 條件式進行時 estaríamos sufriendo，hoy 暗示後果延續至今。",
"【介系詞片語】de encriptar los archivos confidenciales — encargarse de + 不定詞固定搭配，de 引導所負責的動作。",
"【介系詞片語】por una demanda millonaria de los clientes — sufrir por 固定搭配，por 引導痛苦的原因，millonaria 為形容詞修飾 demanda。",
"【時間副詞】hoy（今天）— 置於條件式主句首，強調假設後果在當下時間點仍在持續的現實意義。",
],[
"Condicional irreal de pasado（過去非現實條件句）：si + 虛擬式過去完成時（hubiera encargado）+ 條件式（estaríamos），表示與過去事實相反的假設及其後果，即委員會實際上已加密了檔案。",
"Régimen preposicional（動詞固定介系詞搭配）— encargarse de：反身動詞 encargarse 後接介系詞 de，再接不定詞或名詞，表示負責做某事。",
"Régimen preposicional（動詞固定介系詞搭配）— sufrir por：動詞 sufrir 後接介系詞 por，表示因某事物遭受痛苦。",
"Condicional continuo（條件式進行時）：estaríamos sufriendo = estar 的條件式 + 現在分詞，表示在假設情況下當下正在進行的持續動作，強調後果的當下性。",
],
["comité","seguridad","encargarse","encriptar","archivos","confidenciales","sufrir","demanda","clientes"],
),

("M24-029","Q",
"¿En qué consiste la nueva función de privacidad que la plataforma ha anunciado esta mañana para competir con las aplicaciones de mensajería encriptada?",
"該平台今天早上「宣布」的、用以與加密通訊 APP 競爭的新隱私功能，具體是「包含（由什麼組成）」什麼？",
"Consistir en",
[
"【主要子句（疑問）】¿En qué consiste la nueva función de privacidad...?（新隱私功能包含什麼？）— en qué 為疑問詞組，介系詞 en 前置，consistir en 固定搭配。",
"【關係從句】que la plataforma ha anunciado esta mañana（該平台今天早上宣布的）— 限定性關係從句修飾 la nueva función de privacidad，ha anunciado 為現在完成時。",
"【目的不定詞片語】para competir con las aplicaciones de mensajería encriptada（為了與加密通訊 APP 競爭）— para + 不定詞表目的，competir con 固定搭配。",
"【名詞片語】las aplicaciones de mensajería encriptada — 中心名詞 aplicaciones 加後置限定語 de mensajería，encriptada 為過去分詞形容詞後置修飾 mensajería。",
"【時間狀語】esta mañana（今天早上）— 時間副詞片語，配合現在完成時 ha anunciado，強調今天已完成的動作。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— consistir en：動詞 consistir 後必須接介系詞 en，表示「由...組成、包含...」，是非反身動詞，不能省略 en。例：¿En qué consiste el problema?（問題在哪裡？）",
"Interrogativa con preposición antepuesta（介系詞前置疑問句）：¿En qué? 中介系詞 en 前置，對應 consistir en 的固定搭配，西文疑問句中介系詞不可懸置句尾。",
"Pretérito perfecto compuesto（現在完成時）：ha anunciado 表示今天早上剛完成的動作，與 esta mañana 時間狀語呼應，強調事件的近期性和現實關聯。",
"Competir con（competir con 固定搭配）：動詞 competir 後接介系詞 con，表示與某人或某事物競爭，此為固定搭配，不可與其他介系詞混用。",
],
["función","privacidad","plataforma","anunciar","competir","aplicaciones","mensajería","encriptada"],
),

("M24-030","A",
"Consiste en la destrucción automática de los mensajes después de ser leídos, impidiendo así que nadie se apodere de la información del chat.",
"它「包含」訊息在被閱讀後自動銷毀，藉此「阻礙」任何人「霸佔（據為己有）」聊天室資訊的機會。",
"Consistir en / Apoderarse de",
[
"【主要子句】Consiste en la destrucción automática de los mensajes...（它包含訊息的自動銷毀...）— consistir en 固定搭配，en 後接名詞片語。",
"【時間狀語】después de ser leídos（在被閱讀之後）— después de + 被動不定詞，ser leídos 為被動不定詞，主詞為 los mensajes，表示時間先後。",
"【伴隨狀語（現在分詞）】impidiendo así que nadie se apodere de la información...（藉此阻礙任何人霸佔信息...）— impidiendo 為現在分詞，así 為副詞「藉此、如此」，impedir que + 虛擬式。",
"【名詞子句（虛擬式）】que nadie se apodere de la información del chat — apodere 為虛擬式，受 impedir 觸發，nadie + 虛擬式表示否定主體的虛擬行動。",
"【名詞片語】la destrucción automática de los mensajes — 動詞名詞化 destrucción，automática 前置（例外）或後置均可，de los mensajes 為後置限定語。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— consistir en：動詞 consistir 後接介系詞 en，再接名詞或不定詞，表示由...組成或包含...。",
"Régimen preposicional（動詞固定介系詞搭配）— apoderarse de：反身動詞 apoderarse 後接介系詞 de，表示掌控、據為己有。",
"Infinitivo pasivo（被動不定詞）：ser leídos = ser + 過去分詞，構成被動不定詞，表示訊息被閱讀的被動狀態，過去分詞 leídos 與主詞 mensajes 性數一致（陽性複數）。",
"Impedir que + subjuntivo（impedir que + 虛擬式）：動詞 impedir 表示阻止，後接 que 子句須使用虛擬式（apodere），因為表達說話者的意志或期望阻止的行動。",
],
["destrucción","mensajes","leer","impedir","apoderarse","información","chat"],
),

("M24-031","Q",
"¿Le importaría decirme si usted confía en que las leyes de protección de datos actuales son suficientes para frenar los abusos de las grandes corporaciones?",
"您「介意」告訴我，您是否「信任」現行的數據保護法律足以遏止大型企業的濫用行為嗎？",
"Confiar en",
[
"【主要子句（疑問、禮貌式）】¿Le importaría decirme...?（您介意告訴我...嗎？）— importar 的條件式用於禮貌請求，le 為間接受詞，decirme 為不定詞，me 為附接代詞。",
"【間接疑問句】si usted confía en que las leyes...son suficientes...（您是否信任...法律足夠...）— si 引導間接疑問句作 decirme 的受詞，confiar en + que 子句固定搭配。",
"【名詞子句】que las leyes de protección de datos actuales son suficientes para frenar...（現行法律足以遏止...）— 直述式，confiar en 後接客觀陳述。",
"【目的不定詞片語】para frenar los abusos de las grandes corporaciones（為了遏止大型企業的濫用行為）— para + 不定詞表目的，修飾 suficientes。",
"【名詞片語】las leyes de protección de datos actuales — 中心名詞 leyes 加後置限定語 de protección de datos，形容詞 actuales 後置修飾。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— confiar en：動詞 confiar 後接介系詞 en，可接名詞或 que 子句，表示信任某人或相信某事。例：Confío en que llegará（我相信他會到）。",
"Condicional de cortesía（禮貌條件式）：¿Le importaría...? 使用條件式表示禮貌請求，比直述式 ¿Le importa...? 更婉轉，常用於正式場合或對陌生人的請求。",
"Interrogativa indirecta con si（si 引導間接疑問句）：si 在間接疑問句中表示「是否」，後接陳述句語序，嵌入主句作受詞，不使用倒裝語序。",
"Suficiente para + infinitivo（足以...的結構）：suficiente/s para + 不定詞表示「足夠做某事」，para 引導目的，說明足夠的程度所能達成的結果。",
],
["confiar","leyes","protección","datos","suficiente","frenar","abusos","corporaciones"],
),

("M24-032","A",
"Sinceramente, no confío en ellas; las leyes siempre tardan en adaptarse a las nuevas tecnologías, dejando a los ciudadanos desprotegidos ante el avance digital.",
"老實說，我不「信任」它們；法律在適應新科技方面總是「進展緩慢（拖延）」，這讓公民在數位進步面前「處於」不受保護的狀態。",
"Confiar en / Tardar en",
[
"【副詞修飾語】Sinceramente（老實說）— 語篇副詞，修飾整個句子，表示說話者的誠摯態度，常置於句首以強調坦誠。",
"【主要子句】no confío en ellas（我不信任它們）— confiar en 固定搭配，ellas 指代前文的 las leyes，否定式表達不信任。",
"【並列主句】las leyes siempre tardan en adaptarse a las nuevas tecnologías（法律在適應新科技方面總是拖延）— tardar en + 不定詞固定搭配，siempre 表示習慣性。",
"【伴隨狀語（現在分詞）】dejando a los ciudadanos desprotegidos ante el avance digital（讓公民在數位進步面前不受保護）— dejando 為現在分詞，dejar a alguien + 形容詞表示使某人處於某狀態。",
"【介系詞片語】ante el avance digital（在數位進步面前）— ante 表示「在...面前、面對」，引導所面對的情況。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— tardar en：動詞 tardar 後接介系詞 en，再接不定詞，表示在做某事上花費時間或拖延。例：Tarda en responder（他回覆很慢）。",
"Dejar a alguien + adjetivo（dejar + 受詞 + 形容詞）：dejar 作使役動詞，接受詞 a los ciudadanos 和表語形容詞 desprotegidos，表示使某人處於某種狀態，相當於「讓...變得/處於...」。",
"Ante（介系詞 ante 的用法）：ante + 名詞表示「在...面前、面對某情況」，用於抽象語境時強調面對挑戰或威脅的被動處境。",
"Sinceramente como marcador discursivo（語篇標記副詞）：sinceramente 置於句首作語篇標記，表示說話者即將說出真實想法，引導對前文問題的誠實回應。",
],
["confiar","leyes","tardar","adaptarse","tecnologías","ciudadanos","desprotegido","avance"],
),

("M24-033","R",
"Es una triste realidad; por eso, muchos usuarios optan por cerrar sus perfiles y alejarse de la vida digital activa como medida de precaución.",
"這是個悲傷的現實；因此，許多用戶「選擇（偏向）」關閉他們的個人檔案並「遠離」活躍的數位生活，以此作為預防措施。",
"Optar por / Alejarse de",
[
"【評價句】Es una triste realidad（這是個悲傷的現實）— 主詞 es 指代前文情況，triste 前置於 realidad（例外用法），表示強烈的情感色彩。",
"【連接語】por eso（因此）— 因果連接副詞片語，por eso 引導結果，等同於 por lo tanto，銜接前後句的邏輯關係。",
"【主要子句】muchos usuarios optan por cerrar sus perfiles y alejarse de la vida digital activa（許多用戶選擇關閉個人檔案並遠離活躍數位生活）— optar por + 不定詞固定搭配，alejarse de 固定搭配，兩個不定詞並列。",
"【目的狀語】como medida de precaución（作為預防措施）— como + 名詞作目的或方式狀語，medida de precaución 為複合名詞片語。",
"【名詞片語】la vida digital activa — 中心名詞 vida 加後置形容詞 digital 和 activa，兩者共同後置修飾。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— optar por：動詞 optar 後接介系詞 por，再接名詞或不定詞，表示選擇、偏向某事物。例：Opto por quedarme（我選擇留下）。",
"Régimen preposicional（動詞固定介系詞搭配）— alejarse de：反身動詞 alejarse 後接介系詞 de，表示遠離某人或某事物。例：Se alejó de la ciudad（他遠離了城市）。",
"Por eso（因果連接語）：por eso 為因果連接副詞片語，引導前文原因所導致的結果，位於句首並以逗號與主句隔開，正式程度低於 por lo tanto。",
"Como + sustantivo（como + 名詞表比較或方式）：como medida de precaución 表示「作為預防措施」，como 引導名詞作補語，說明行動的性質或目的。",
],
["usuarios","optar","cerrar","perfiles","alejarse","vida","digital","medida","precaución"],
),

("M24-034","D",
"El hacker se aprovechó de una vulnerabilidad en el sistema operativo, logrando acceder al servidor donde la empresa almacenaba los datos de pago.",
"駭客「利用了（佔便宜）」作業系統中的一個漏洞，成功進入了公司「存放」付款數據的伺服器。",
"Aprovecharse de",
[
"【主要子句】El hacker se aprovechó de una vulnerabilidad en el sistema operativo（駭客利用了作業系統中的一個漏洞）— aprovecharse de 固定搭配，en el sistema operativo 為地點介系詞片語修飾 vulnerabilidad。",
"【結果狀語（現在分詞）】logrando acceder al servidor...（成功進入伺服器...）— lograr + 不定詞表示成功做到，現在分詞 logrando 引導結果狀語，描述利用漏洞後達成的結果。",
"【關係從句】donde la empresa almacenaba los datos de pago（公司存放付款數據的地方）— donde 引導地點關係從句，修飾 el servidor，almacenaba 為過去未完成時表習慣性過去動作。",
"【介系詞片語】de una vulnerabilidad en el sistema operativo — aprovecharse de 的受詞，en el sistema operativo 為後置地點修飾語。",
"【名詞片語】los datos de pago — 中心名詞 datos 加後置限定語 de pago，指付款相關數據。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— aprovecharse de：反身動詞 aprovecharse 後接介系詞 de，表示利用、佔...的便宜，帶有負面語義，暗示不正當利用。例：Se aprovechó de su ingenuidad（他利用了她的天真）。",
"Lograr + infinitivo（lograr + 不定詞）：lograr 後接原形動詞，表示「成功做到...」，強調克服困難後達成的結果，此處以現在分詞形式 logrando 作狀語。",
"Pretérito imperfecto en relativa（關係從句中的過去未完成時）：almacenaba 使用過去未完成時，表示在過去某時間段內的習慣性動作（持續存放數據），而非單次完成的動作。",
"Donde（地點關係代詞）：donde 引導地點關係從句，可替換 en que 或 en el cual，修飾表示地點的先行詞 el servidor。",
],
["hacker","aprovecharse","vulnerabilidad","sistema","operativo","acceder","servidor","empresa","almacenar","datos"],
),

("M24-035","Q",
"¿Cómo reaccionó el director cuando se enteró de que las fotos del prototipo secreto estaban circulando por canales de comunicación no oficiales?",
"當主管「獲悉」祕密原型的照片「正在」非官方通訊管道「流傳」時，他「如何反應」？",
"Enterarse de",
[
"【主要子句（疑問）】¿Cómo reaccionó el director...?（主管如何反應？）— cómo 為方式疑問詞，reaccionó 為簡單過去時，疑問句動詞先於主詞。",
"【時間從句】cuando se enteró de que...（當他獲悉...時）— cuando 引導時間從句，enterarse de + que 子句固定搭配，enteró 為簡單過去時。",
"【名詞子句】que las fotos del prototipo secreto estaban circulando por canales...（照片正在管道中流傳）— estaban circulando 為過去進行時，表示獲悉時正在進行的動作。",
"【過去進行時】estaban circulando（正在流傳）— estar 的過去未完成時 + 現在分詞，描述在過去某時間點正在持續進行的動作。",
"【介系詞片語】por canales de comunicación no oficiales — por 表示「經由、通過」，引導路徑或媒介，canales 為複數名詞。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— enterarse de：動詞 enterarse 後接介系詞 de，引導 que 子句，表示獲悉某事。",
"Pretérito imperfecto progresivo（過去進行時）：estaban circulando = estar（過去未完成時）+ 現在分詞，強調在過去某參照時間點動作正在持續進行，此處指主管獲悉消息時照片仍在流傳中。",
"Por（表示通過、經由的介系詞）：por canales 中的 por 表示「通過、經由」某管道，強調訊息傳播的路徑，不同於表示原因或代理人的 por。",
"Prototipo secreto（後置形容詞）：secreto 後置修飾名詞 prototipo，此為西文形容詞常見位置，後置強調描述性；若前置（secreto prototipo）則帶有主觀強調語氣。",
],
["reaccionar","director","enterarse","fotos","prototipo","circular","canales","comunicación"],
),

("M24-036","A",
"Se enfadó con el equipo de desarrollo, acusándolos de haber sido descuidados y de no haber cumplido con las normas básicas de confidencialidad de la firma.",
"他對開發團隊「感到非常生氣」，「指責他們」太過粗心大意且「沒有履行」公司基本的保密規範。",
"Enfadarse con / Acusar de",
[
"【主要子句】Se enfadó con el equipo de desarrollo（他對開發團隊感到生氣）— enfadarse con 固定搭配，con 引導生氣的對象。",
"【伴隨狀語（現在分詞）】acusándolos de haber sido descuidados y de no haber cumplido...（指責他們粗心且未履行...）— acusar de 固定搭配，los 為附接代詞指代 el equipo，haber + 過去分詞為完成不定詞。",
"【並列介系詞片語】de haber sido descuidados y de no haber cumplido con las normas...— 兩個 de + 完成不定詞並列，共同作 acusar de 的受詞，說明指責的兩項內容。",
"【完成不定詞被動】haber sido descuidados — haber + sido + 過去分詞，構成完成不定詞被動，表示在指責時間點之前已是粗心的狀態。",
"【介系詞片語】con las normas básicas de confidencialidad de la firma — cumplir con 固定搭配，以 con 引導所履行的對象，雙重後置限定語說明規範的性質和所屬。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— enfadarse con：反身動詞 enfadarse 後接介系詞 con，表示對某人或某事感到生氣。例：Se enfadó con su jefe（他對上司感到生氣）。",
"Régimen preposicional（動詞固定介系詞搭配）— acusar de：動詞 acusar 後接介系詞 de，引導被指責的行為，可接名詞或不定詞（包括完成不定詞）。例：Lo acusan de robar（他們指控他偷竊）。",
"Infinitivo perfecto（完成不定詞）：haber + 過去分詞構成完成不定詞，表示早於主句動作完成的動作，haber sido descuidados 和 no haber cumplido 均表示在主管生氣之前已發生的行為。",
"Cumplir con（cumplir con 固定搭配）：動詞 cumplir 後接介系詞 con，表示履行、遵守某義務或規範，con 不可省略。例：Cumple con su deber（他履行職責）。",
],
["enfadarse","equipo","desarrollo","acusar","descuidado","cumplir","normas","confidencialidad","firma"],
),

("M24-037","R",
"¡Qué situación tan tensa! Me imagino que el responsable del descuido se arrepentirá de no haber guardado el material en la caja fuerte digital.",
"真是太緊張的局勢了！我「想像」該疏忽的負責人現在一定「會後悔」當初沒將材料存放在數位保險箱裡。",
"Arrepentirse de",
[
"【感嘆語】¡Qué situación tan tensa!（真是太緊張的局勢了！）— qué + 名詞 + tan + 形容詞構成感嘆句，強調程度，tan 替換 muy，語氣更強烈。",
"【主要子句】Me imagino que el responsable del descuido se arrepentirá...（我想像負責人將會後悔...）— imaginar(se) que + 直述式，表示說話者的推測，arrepentirse 為未來時。",
"【名詞子句（直述式）】que el responsable del descuido se arrepentirá de no haber guardado...（負責人將會後悔沒保存...）— arrepentirse de + 完成不定詞，表示對過去行為的後悔。",
"【介系詞片語（完成不定詞否定）】de no haber guardado el material en la caja fuerte digital — arrepentirse de 的受詞，no haber + 過去分詞表示否定的過去動作，後悔沒做某事。",
"【名詞片語】la caja fuerte digital — 複合名詞 caja fuerte（保險箱）加後置形容詞 digital，指數位保險箱或加密儲存設備。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— arrepentirse de：反身動詞 arrepentirse 後接介系詞 de，引導名詞或（完成）不定詞，表示後悔做了或沒做某事。例：Se arrepiente de haberlo dicho（他後悔說了那句話）。",
"Infinitivo perfecto negativo（否定完成不定詞）：no haber guardado 表示「沒有保存」，no 置於 haber 之前否定整個完成不定詞，描述所後悔的過去遺漏動作。",
"Futuro de probabilidad（推測未來時）：se arrepentirá 使用未來時，在此語境中（配合 me imagino）表示說話者對未來的合理推測，帶有強烈的主觀判斷。",
"Qué + sustantivo + tan + adjetivo（感嘆句結構）：¡Qué situación tan tensa! 為固定感嘆句型，tan 為程度副詞修飾形容詞，此結構比 ¡Qué situación más tensa! 更常見於口語。",
],
["imaginar","responsable","descuido","arrepentirse","guardar","material","caja","digital"],
),

("M24-038","D",
"Si la red social nos obligara a rellenar un cuestionario sobre nuestra vida privada, muchos de nosotros dejaríamos de usar la aplicación de inmediato.",
"如果社交網路「強制要求」我們填寫一份關於私生活的問卷，我們之中的許多人「將會」立即「停止」使用該 APP。",
"Obligar a / Dejar de",
[
"【條件從句（虛擬式過去）】Si la red social nos obligara a rellenar un cuestionario...（如果社交網路強制要求我們填寫問卷...）— si + 虛擬式過去時，表示假設性條件，nos 為間接受詞。",
"【主句（條件式）】muchos de nosotros dejaríamos de usar la aplicación de inmediato（我們之中許多人將立即停止使用 APP）— 條件式 dejaríamos，dejar de + 不定詞固定搭配。",
"【介系詞片語（話題）】sobre nuestra vida privada（關於私生活）— sobre 引導話題介系詞片語，修飾 cuestionario，說明問卷的主題。",
"【代詞片語】muchos de nosotros（我們之中的許多人）— muchos 作代詞，de nosotros 為後置限定語，強調說話者群體中的多數人。",
"【時間狀語】de inmediato（立即）— 慣用副詞片語，表示立刻、馬上，等同於 inmediatamente。",
],[
"Obligar a alguien a + infinitivo（obligar a 的雙重 a 結構）：obligar 接間接受詞（nos）表示被強制者，再接 a + 不定詞表示被強制做的事，構成雙重 a 結構（一個為間接受詞標記，一個為動詞搭配介系詞）。",
"Dejar de + infinitivo（dejar de + 不定詞）：表示「停止做某事」，固定搭配，不定詞說明被中斷的動作。",
"Condicional irreal de presente（現在非現實條件句）：si + 虛擬式過去時（obligara）+ 條件式（dejaríamos），表示假設性情況，暗示社交網路實際上並未強制要求填問卷。",
"De inmediato（副詞性片語）：de inmediato 為固定副詞片語，表示「立即、馬上」，常用於正式或書面語境，口語中也可用 enseguida 或 de repente（後者含「突然」之義）。",
],
["red","social","obligar","rellenar","cuestionario","vida","privada","dejar","usar","aplicación"],
),

("M24-039","Q",
"¿De qué depende que un usuario decida borrar su huella digital y desconectarse de internet para siempre, según las investigaciones más recientes?",
"根據最新的研究，一個用戶「決定」清除其數位足跡並永遠「切斷與」網路的聯繫，這究竟「取決於」什麼？",
"Depender de / Desconectarse de",
[
"【主要子句（疑問）】¿De qué depende que un usuario decida borrar su huella digital...?（取決於什麼...？）— de qué 為疑問詞組，介系詞 de 前置，depender de + que 虛擬式。",
"【名詞子句（虛擬式）】que un usuario decida borrar su huella digital y desconectarse de internet para siempre（用戶決定清除數位足跡並永遠切斷網路連接）— decida 為虛擬式，受 depender de 觸發。",
"【並列不定詞片語】borrar su huella digital y desconectarse de internet para siempre — 兩個不定詞並列，共同作 decida 的受詞，desconectarse de 固定搭配。",
"【時間狀語】para siempre（永遠）— 副詞片語，修飾 desconectarse，表示動作的永久性。",
"【附加說明】según las investigaciones más recientes（根據最新研究）— según 為介系詞，引導來源或依據，置於句末作補充說明。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— depender de：動詞 depender 後接介系詞 de，表示取決於某事物。",
"Régimen preposicional（動詞固定介系詞搭配）— desconectarse de：反身動詞 desconectarse 後接介系詞 de，表示切斷與某事物的連接或脫離某環境。例：Se desconectó de las redes（他脫離了社交媒體）。",
"Subjuntivo tras impersonales（非人稱結構後接虛擬式）：¿De qué depende que...? 中，depender de que 後須使用虛擬式（decida），因為表達的是不確定的假設情況而非具體事實。",
"Según（根據介系詞）：según + 名詞或動詞，表示依據某來源或根據某人的說法，置於句首或句末均可，是引用來源的正式表達方式。",
],
["usuario","decidir","borrar","huella","digital","desconectarse","internet","investigaciones"],
),

("M24-040","A",
"Depende sobre todo de su nivel de saturación mental; cuando la gente se cansa de recibir publicidad dirigida, comienza a valorar más su anonimato.",
"這主要「取決於」其精神飽和程度；當人們對於接收精準投放廣告「感到厭倦」時，便「開始」更看重自身的匿名性。",
"Depender de / Cansarse de",
[
"【主要子句】Depende sobre todo de su nivel de saturación mental（這主要取決於其精神飽和程度）— depender de 固定搭配，sobre todo 為強調副詞片語「主要地、首先」。",
"【時間從句】cuando la gente se cansa de recibir publicidad dirigida（當人們厭倦於接收精準廣告時）— cuando 引導時間從句，cansarse de + 不定詞固定搭配。",
"【結果主句】comienza a valorar más su anonimato（便開始更看重其匿名性）— empezar a/comenzar a + 不定詞表示動作起始，más 表示程度增加。",
"【介系詞片語】de recibir publicidad dirigida — cansarse de + 不定詞的受詞，說明厭倦的對象。",
"【名詞片語】publicidad dirigida — 中心名詞 publicidad 加後置過去分詞 dirigida，指「精準投放的廣告」。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— cansarse de：反身動詞 cansarse 後接介系詞 de，再接名詞或不定詞，表示對某事感到厭倦。例：Me canso de esperar（我厭倦了等待）。",
"Comenzar a + infinitivo（comenzar a + 不定詞）：動詞 comenzar 後接介系詞 a，再接不定詞，表示開始做某事，與 empezar a 同義可互換。",
"Sobre todo（強調副詞片語）：sobre todo 表示「主要地、首先、尤其」，修飾動詞或整個句子，在語義上強調所修飾成分的重要性或優先性。",
"Publicidad dirigida（精準廣告）：dirigida 為過去分詞轉化的形容詞，後置修飾 publicidad，表示「被定向投放的廣告」，即根據用戶數據精準推送的廣告內容。",
],
["depender","saturación","mental","gente","cansarse","recibir","publicidad","comenzar","valorar","anonimato"],
),

("M24-041","Q",
"¿Por qué el departamento legal insiste en que debemos pedir permiso por escrito cada vez que queramos publicar el testimonio de un cliente en la web?",
"為什麼法務部「堅持認為」，每當我們「想要」在網頁上發布客戶的證言時，我們「必須」每次都取得書面許可？",
"Insistir en",
[
"【主要子句（疑問）】¿Por qué el departamento legal insiste en que...?（為什麼法務部堅持...？）— insistir en + que 子句固定搭配，疑問句以 por qué 引導。",
"【名詞子句（虛擬式）】que debemos pedir permiso por escrito cada vez que queramos publicar...（我們必須每次在想要發布時取得書面許可）— deber 表示義務，直述式；cada vez que + 虛擬式 queramos 表示每當（不確定的重複情況）。",
"【時間狀語】cada vez que queramos publicar el testimonio de un cliente en la web（每當我們想要在網頁上發布客戶證言時）— cada vez que + 虛擬式，表示重複性條件。",
"【介系詞片語（方式）】por escrito（以書面形式）— por + 名詞作方式狀語，表示以書面方式，是固定搭配。",
"【名詞片語】el testimonio de un cliente — 中心名詞 testimonio 加後置限定語 de un cliente，指客戶的證言或推薦語。",
],[
"Insistir en + que + indicativo/subjuntivo（insistir en 的語式選擇）：insistir en + que 後接直述式時表示堅持陳述某事實；後接虛擬式時表示堅持要求某人做某事。此句中 debemos 為直述式，表示法務部堅持陳述一項規則。",
"Cada vez que + subjuntivo（每當...的虛擬式）：cada vez que 引導重複性時間從句，當先行詞不確定或動作尚未發生時，須使用虛擬式（queramos），表示每次想要發布的假設情況。",
"Por escrito（書面形式慣用語）：por escrito 為固定副詞片語，表示「以書面形式」，常與 pedir、comunicar、confirmar 等動詞搭配使用。",
"Deber + infinitivo（deber + 不定詞表義務）：debemos pedir 表示「我們必須索取」，deber 為情態動詞表示義務，比 tener que 語氣更正式，常見於法律或正式文件。",
],
["departamento","legal","insistir","pedir","permiso","publicar","testimonio","cliente","web"],
),

("M24-042","A",
"Insisten en ello para protegernos de posibles demandas por derechos de imagen, evitando de este modo que la empresa se vea envuelta en litigios costosos.",
"他們「堅持如此」是為了「保護我們免受」可能的肖像權訴訟，藉此「避免」公司陷入昂貴訴訟的境地。",
"Insistir en / Proteger de",
[
"【主要子句】Insisten en ello（他們堅持如此）— insistir en 固定搭配，ello 為中性代詞指代前文提及的要求行為。",
"【目的狀語】para protegernos de posibles demandas por derechos de imagen（為了保護我們免受肖像權訴訟）— para + 不定詞表目的，proteger de 固定搭配，nos 為附接代詞。",
"【伴隨狀語（現在分詞）】evitando de este modo que la empresa se vea envuelta en litigios costosos（藉此避免公司陷入昂貴訴訟）— evitando 為現在分詞，de este modo 為方式副詞片語，evitar que + 虛擬式。",
"【名詞子句（虛擬式）】que la empresa se vea envuelta en litigios costosos — vea 為虛擬式，受 evitar 觸發，verse envuelto en 表示「陷入、被捲入」。",
"【介系詞片語】por derechos de imagen — por 引導原因，derechos de imagen 為「肖像權」的法律術語。",
],[
"Proteger de（proteger de 固定搭配）：動詞 proteger 後接介系詞 de，表示保護某人或某物免受某事物的侵害。例：La vacuna nos protege de la enfermedad（疫苗保護我們免受疾病）。",
"Evitar que + subjuntivo（evitar que + 虛擬式）：動詞 evitar 表示避免，後接 que 子句須使用虛擬式（vea），因為表達說話者希望阻止發生的事。",
"Verse envuelto en（verse envuelto en 固定搭配）：反身動詞 verse 表示「發現自己處於某狀態」，envuelto en 表示「陷入、被捲入」某事，常用於描述被動捲入負面事件。",
"De este modo（方式副詞片語）：de este modo 表示「以這種方式、藉此」，起語篇銜接功能，引導前述動作（堅持要求）如何導致後述結果（避免訴訟）。",
],
["insistir","proteger","demandas","derechos","imagen","evitar","empresa","litigios"],
),

("M24-043","R",
"Me parece una excelente estrategia preventiva; es mejor dedicar tiempo a conseguir las autorizaciones correctas que sufrir por un error legal evitable.",
"這在我看來是個極佳的預防策略；將時間「投入到」取得正確授權上，也比為了一個可避免的法律錯誤而「遭受痛苦」要好得多。",
"Dedicar a / Sufrir por",
[
"【評價句】Me parece una excelente estrategia preventiva（這在我看來是個極佳的預防策略）— 動詞 parecer 以間接受詞 me 表示主觀評價，省略了受詞 eso。",
"【比較主句】es mejor dedicar tiempo a conseguir las autorizaciones correctas（將時間投入取得授權更好）— es mejor + 不定詞，比較結構的主項，dedicar a + 不定詞固定搭配。",
"【比較從句】que sufrir por un error legal evitable（比為了可避免的法律錯誤遭受痛苦）— que 引導比較的次項，sufrir por 固定搭配，evitable 為形容詞修飾 error。",
"【介系詞片語】a conseguir las autorizaciones correctas — dedicar a + 不定詞，表示將（時間等）投入於做某事。",
"【名詞片語】un error legal evitable — 中心名詞 error 加後置形容詞 legal（類型）和 evitable（性質）。",
],[
"Es mejor + infinitivo + que + infinitivo（比較句型）：es mejor A que B 表示「A 比 B 更好」，A 和 B 均為不定詞，構成動詞不定詞的比較結構，是常見的評價性表達。",
"Dedicar tiempo a + infinitivo（dedicar 時間搭配）：dedicar + 時間/精力 + a + 不定詞，表示將時間或精力投入於做某事，a 為固定搭配介系詞。",
"Régimen preposicional（動詞固定介系詞搭配）— sufrir por：動詞 sufrir 後接介系詞 por，表示因某事遭受痛苦或承擔後果。",
"Adjetivo evitable（形容詞 evitable 的構詞）：evitable 由動詞 evitar 派生而來，後綴 -able 表示「可被...的」，evitable 即「可被避免的」，此類形容詞在西文中非常能產。",
],
["estrategia","preventiva","dedicar","tiempo","conseguir","autorizaciones","sufrir","error","legal"],
),

("M24-044","D",
"El nuevo buscador se caracteriza por no almacenar el historial de navegación, ofreciendo un entorno seguro para quienes huyen de la vigilancia comercial.",
"這款新搜尋引擎的「特點在於」不儲存瀏覽歷史記錄，為那些「躲避」商業監視的人「提供」了一個安全的環境。",
"Caracterizarse por / Huir de",
[
"【主要子句】El nuevo buscador se caracteriza por no almacenar el historial de navegación（新搜尋引擎的特點在於不儲存瀏覽歷史）— caracterizarse por 固定搭配，no 否定不定詞。",
"【伴隨狀語（現在分詞）】ofreciendo un entorno seguro para quienes huyen de la vigilancia comercial（為躲避商業監視的人提供安全環境）— ofreciendo 為現在分詞作伴隨狀語，描述特徵帶來的附帶結果。",
"【關係從句（虛擬式）】quienes huyen de la vigilancia comercial（那些躲避商業監視的人）— quienes 為關係代詞（等同於 las personas que），huyen 為直述式，因指具體現實中的人群。",
"【介系詞片語】de la vigilancia comercial — huir de 固定搭配，de 引導所逃避的對象。",
"【名詞片語】un entorno seguro — 中心名詞 entorno 加後置形容詞 seguro，指安全的環境或生態系統。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— caracterizarse por：反身動詞 caracterizarse 後接介系詞 por，再接名詞或不定詞，表示以...為特徵。例：Se caracteriza por su honestidad（他以誠實為特點）。",
"Régimen preposicional（動詞固定介系詞搭配）— huir de：動詞 huir 後接介系詞 de，表示逃離或躲避某人或某事物。例：Huye de los problemas（他逃避問題）。",
"Negación del infinitivo（不定詞的否定）：no almacenar，以 no 置於不定詞前構成否定，描述該搜尋引擎不做的特定動作，強調其隱私保護特性。",
"Quienes（關係代詞 quienes）：quienes 為複數關係代詞，指代人，等同於 las personas que，常用於無先行詞的自由關係從句，作後文動詞 ofreciendo 的間接受詞。",
],
["buscador","caracterizarse","almacenar","historial","navegación","ofrecer","entorno","huir","vigilancia"],
),

("M24-045","Q",
"¿A qué se arriesga una corporación si se descubre que vende los datos confidenciales de sus usuarios a agencias de marketing sin autorización?",
"如果一間企業「被發現」在未經授權的情況下將用戶的機密數據「販售」给行銷機構，它「將面臨」什麼樣的「風險」？",
"Arriesgarse a",
[
"【主要子句（疑問）】¿A qué se arriesga una corporación...?（企業面臨什麼風險？）— a qué 為疑問詞組，介系詞 a 前置，arriesgarse a 固定搭配。",
"【條件從句】si se descubre que vende los datos confidenciales...（如果被發現販售機密數據...）— si + 直述式現在時表現實條件，se descubre 為被動反身式表示被發現。",
"【名詞子句】que vende los datos confidenciales de sus usuarios a agencias de marketing sin autorización（販售用戶機密數據給行銷機構）— 直述式子句作 descubrirse 的受詞，陳述被發現的事實。",
"【介系詞片語（方式）】sin autorización（未經授權）— sin + 名詞作條件狀語，表示缺少必要授權，強調行為的違規性。",
"【名詞片語】los datos confidenciales de sus usuarios — 中心名詞 datos 加後置形容詞 confidenciales 和後置限定語 de sus usuarios。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— arriesgarse a：反身動詞 arriesgarse 後接介系詞 a，再接名詞或不定詞，表示冒著...的風險。例：Se arriesga a perder todo（他冒著失去一切的風險）。",
"Interrogativa con preposición antepuesta（介系詞前置疑問句）：¿A qué? 中介系詞 a 前置，對應 arriesgarse a 的固定搭配，西文規範不允許介系詞懸置句尾。",
"Se impersonal（非人稱反身式）：se descubre 為非人稱被動結構，表示「被發現」，相當於英文的 it is discovered that，主詞為泛指的不確定者。",
"Sin + sustantivo（sin + 名詞表條件缺失）：sin autorización 表示「在沒有授權的情況下」，構成否定條件狀語，強調行為缺少法律或道德許可。",
],
["corporación","arriesgarse","descubrir","vender","datos","confidenciales","usuarios","agencias","marketing","autorización"],
),

("M24-046","A",
"Se arriesga a multas multimillonarias que podrían llevarla a la quiebra, además de a una pérdida irreparable de reputación que la destruiría comercialmente.",
"它「將面臨」可能導致其破產的數百萬美元罰款「風險」，此外還面臨著將在商業上摧毀它的無法挽回的商譽損失。",
"Arriesgarse a / Además de a",
[
"【主要子句】Se arriesga a multas multimillonarias que podrían llevarla a la quiebra（它面臨可能導致破產的鉅額罰款風險）— arriesgarse a 固定搭配，la 為附接代詞指代 la corporación。",
"【關係從句】que podrían llevarla a la quiebra（可能導致其破產的）— 情態動詞 podrían 表示可能性，llevar a alguien a + 名詞表示使某人達到某境地。",
"【並列補充】además de a una pérdida irreparable de reputación（此外還有無法挽回的商譽損失）— además de 後接介系詞 a，因承接 arriesgarse a 的搭配，此為雙介系詞結構。",
"【關係從句】que la destruiría comercialmente（將在商業上摧毀它的）— 條件式 destruiría 表示假設後果，comercialmente 為方式副詞。",
"【名詞片語】una pérdida irreparable de reputación — 中心名詞 pérdida 加後置形容詞 irreparable 和後置限定語 de reputación。",
],[
"Arriesgarse a（arriesgarse a 的受詞類型）：arriesgarse a 後可接名詞（如 multas）或不定詞，此句接名詞作直接受詞，表示面臨某種具體風險。",
"Además de a（además de 後接介系詞的雙介系詞結構）：cuando además de 後的成分需要特定介系詞（此處為 a，因承接 arriesgarse a），須保留原介系詞，形成 además de a 的雙介系詞結構，是西文文法的特殊要求。",
"Llevar a alguien a + sustantivo（使某人達到某境地）：llevar 作使役動詞，接受詞和 a + 名詞，表示導致某人或某事物達到某種結果或境地。例：Lo llevó a la ruina（這導致了他的破產）。",
"Irreparable（形容詞 irreparable）：由前綴 ir-（否定）加形容詞 reparable（可修復的）構成，表示「無法修復的、不可挽回的」，ir- 為常見否定前綴（ir-, in-, im-，根據後接子音變化）。",
],
["arriesgarse","multas","quiebra","pérdida","reputación","destruir","comercialmente"],
),

("M24-047","R",
"¡Es el castigo que se merecen! Ninguna empresa debería aprovecharse de la buena fe de las personas para lucrarse a costa de su intimidad protegida.",
"這是他們應得的懲罰！沒有任何公司應該「利用（佔便宜）」人們的善意，來以犧牲其受保護的隱私為代價「獲利」。",
"Aprovecharse de / Lucrarse a",
[
"【感嘆語】¡Es el castigo que se merecen!（這是他們應得的懲罰！）— 關係從句 que se merecen 修飾 el castigo，merecer 表示應得，語氣強烈表達道德判斷。",
"【主要子句】Ninguna empresa debería aprovecharse de la buena fe de las personas（沒有任何公司應該利用人們的善意）— ninguna + 名詞為否定泛指，deber 的條件式 debería 表示道德上的義務。",
"【目的不定詞片語】para lucrarse a costa de su intimidad protegida（為了以犧牲其受保護的隱私為代價獲利）— para + 不定詞表目的，a costa de 固定搭配表示以...為代價。",
"【介系詞片語】de la buena fe de las personas — aprovecharse de 固定搭配，de 引導所利用的對象，buena fe 為固定名詞片語「善意、誠信」。",
"【名詞片語】su intimidad protegida — 物主形容詞 su 加中心名詞 intimidad，過去分詞 protegida 後置修飾，指「受保護的隱私」。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— aprovecharse de：反身動詞 aprovecharse 後接介系詞 de，表示利用、佔...的便宜，帶有貶義。",
"A costa de（以...為代價）：a costa de + 名詞為固定介系詞片語，表示「以...為代價」，常用於描述不合理的犧牲或損失，帶有負面語氣。例：Lo logró a costa de su salud（他以健康為代價達成了目標）。",
"Deber condicional（deber 的條件式表道德義務）：debería 為 deber 的條件式，比直述式 debe 更婉轉，在否定句中表示「本不應該...」，帶有道德批判語氣。",
"Ninguno/a（否定形容詞 ninguno/a）：ninguna empresa 表示「沒有任何一家公司」，為完全否定，作主詞時謂語動詞用第三人稱單數，ninguna 在名詞前去掉詞尾 -o（若陰性保留 -a）。",
],
["empresa","aprovecharse","buena","fe","personas","lucrarse","intimidad","protegida"],
),

("M24-048","D",
"Si el administrador de la red se hubiera fijado en el tráfico inusual del servidor, el robo de las cuentas se habría evitado antes de que fuera tarde.",
"如果網路管理員當初有「注意到（過）」伺服器異常的流量，帳號遭竊取的事在為時已晚前本「就會被避免」了。",
"Fijarse en",
[
"【條件從句（虛擬式過去完成）】Si el administrador de la red se hubiera fijado en el tráfico inusual del servidor（如果網路管理員當初注意到伺服器異常流量）— si + 虛擬式過去完成時，表示與過去事實相反的假設。",
"【主句（條件式完成時被動）】el robo de las cuentas se habría evitado（帳號遭竊取的事就會被避免）— 條件式完成時 habría + 過去分詞，被動結構 se habría evitado。",
"【時間狀語】antes de que fuera tarde（在為時已晚之前）— antes de que + 虛擬式，fuera 為 ser 的虛擬式過去時，表示參照時間點的假設。",
"【介系詞片語】en el tráfico inusual del servidor — fijarse en 固定搭配，en 引導所注意到的對象。",
"【名詞片語】el tráfico inusual del servidor — 中心名詞 tráfico 加後置形容詞 inusual，del servidor 為後置限定語。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— fijarse en：反身動詞 fijarse 後接介系詞 en，表示注意到、注意觀察某事物。例：Fíjate en los detalles（注意細節）。",
"Condicional irreal de pasado（過去非現實條件句）：si + 虛擬式過去完成時（hubiera fijado）+ 條件式完成時（habría evitado），表示與過去事實完全相反的假設及其後果。",
"Voz pasiva refleja（反身被動語態）：se habría evitado 為條件式完成時的反身被動，相當於 habría sido evitado，主詞 el robo 為被動受事者，結構更簡潔。",
"Antes de que + subjuntivo（antes de que + 虛擬式）：antes de que 後必須使用虛擬式（fuera），因為表達的是在某行動發生之前的時間，為假設性時間點。",
],
["administrador","red","fijarse","tráfico","inusual","servidor","robo","cuentas","evitar"],
),

("M24-049","Q",
"¿Usted cree que para el final de esta década la sociedad habrá aprendido a convivir con la inteligencia artificial sin renunciar a la privacidad individual?",
"您「認為」到這個十年結束時，社會「將會學會與」人工智慧共存，且同時不「放棄」個人隱私嗎？",
"Aprender a / Renunciar a",
[
"【主要子句（疑問）】¿Usted cree que...?（您認為...嗎？）— creer que + 直述式，疑問句以升調表示，usted 為正式第二人稱。",
"【名詞子句（未來完成時）】que para el final de esta década la sociedad habrá aprendido a convivir...（社會將在十年末學會共存...）— 未來完成時 habrá + 過去分詞，表示在未來某時間點之前將已完成的動作。",
"【時間狀語】para el final de esta década（到這個十年結束時）— para + 名詞片語作時間狀語，表示期限，強調在某時間點之前完成。",
"【不定詞片語】a convivir con la inteligencia artificial（與人工智慧共存）— aprender a + 不定詞，convivir con 固定搭配表示與某事物共同生活。",
"【否定不定詞片語】sin renunciar a la privacidad individual（不放棄個人隱私）— sin + 不定詞表示缺少某伴隨動作，renunciar a 固定搭配。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— aprender a：動詞 aprender 後接介系詞 a，再接不定詞，表示學會做某事。例：Aprende a cocinar（他學做飯）。",
"Régimen preposicional（動詞固定介系詞搭配）— renunciar a：動詞 renunciar 後接介系詞 a，表示放棄、拋棄某事物。例：Renunció a su cargo（他辭去職務）。",
"Futuro perfecto（未來完成時）：habrá aprendido = haber 的未來時（habrá）+ 過去分詞，表示在未來某參照時間點（para el final de esta década）之前將已完成的動作。",
"Para + tiempo（para 表示期限的時間狀語）：para + 時間表示「到...為止、在...之前」，強調完成期限，配合未來完成時使用，說明動作的截止時間點。",
],
["sociedad","aprender","convivir","inteligencia","artificial","renunciar","privacidad","individual"],
),

("M24-050","R",
"Ha sido un placer debatir sobre estos temas; si todos contribuimos a exigir más transparencia, lograremos que el futuro digital sea más respetuoso y seguro.",
"辯論這些話題真是件「愉快」的事；如果我們大家都「有助於（貢獻）」要求更多透明度，我們將能讓數位未來「變得」更具尊重且安全。",
"Contribuir a / Subjuntivo",
[
"【評價句】Ha sido un placer debatir sobre estos temas（辯論這些話題真是件愉快的事）— ha sido 為現在完成時，表示剛結束的愉快經歷，debatir 為不定詞作主詞。",
"【條件從句】si todos contribuimos a exigir más transparencia（如果我們大家都有助於要求更多透明度）— si + 直述式現在時，contribuir a + 不定詞固定搭配，此處表示現實條件假設。",
"【主句（未來時）】lograremos que el futuro digital sea más respetuoso y seguro（我們將能讓數位未來更具尊重且安全）— lograr + que 虛擬式，sea 為 ser 的虛擬式。",
"【名詞子句（虛擬式）】que el futuro digital sea más respetuoso y seguro — sea 為虛擬式，受 lograr 觸發，表示希望達成的結果狀態。",
"【介系詞片語（話題）】sobre estos temas — sobre 引導話題，estos temas 以指示形容詞 estos 指代討論中涉及的所有話題。",
],[
"Régimen preposicional（動詞固定介系詞搭配）— contribuir a：動詞 contribuir 後接介系詞 a，再接名詞或不定詞，表示有助於或貢獻於某事。",
"Lograr que + subjuntivo（lograr que + 虛擬式）：動詞 lograr 表示成功達成，後接 que 子句須使用虛擬式（sea），因為表達說話者期望達成的目標狀態。",
"Si + indicativo presente（現實條件句）：si + 直述式現在時，主句用未來時（lograremos），構成現實條件句，表示可能實現的條件及其後果，與反現實條件句（si + 虛擬式）不同。",
"Ha sido un placer + infinitivo（感謝告別慣用語）：ha sido un placer + 不定詞為固定表達，意為「做...是一種榮幸/愉快」，常用於對話結束時表達愉快的感謝，語氣正式而親切。",
],
["placer","debatir","temas","contribuir","exigir","transparencia","lograr","futuro","digital","seguro"],
),
]

count = 0
for entry in CARDS:
    old_id, ctype, es, zh, gram_title, parse_pts, gram_pts, keywords = entry
    new_id = convert_id(old_id)
    write_card(new_id, ctype, es, zh, gram_title, parse_pts, gram_pts, keywords)
    count += 1
    print(f"OK: {new_id}")

print(f"\nPart 2 done: {count} cards")

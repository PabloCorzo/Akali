BAD_WORDS = [
    # --- Violencia sexual / abuso ---
    "violación", "violador", "violar", "vi0lar", "v1olar",
    "violando", "violada",
    "incesto", "pederastia", "pedo",
    "abuso", "abusar", "abuso infantil",
    "pornografía infantil",

    # --- Palabras sensibles sueltas (para filtro, no contexto) ---
    "menor",

    # --- Follar / variantes ---
    "f0llar", "fo11ar", "f0ll4r", "f0ll@r", "f*llar",
    "f0ll-ar", "f0ll.r", "f0ll4rX", "foll4r_",
    "foLL4r", "f0lL4r", "f0|lar", "f°llar",
    "f0l|ar", "f0ll4rXX", "f0l1ar", "f0l!ar",
    "f0l-l4r", "fol-l4r", "foll4rZ", "f0LL4R",
    "f0lLar~", "foll4r!!", "f0ll@r#", "f0l|_ar",
    "f0ll4r??", "f0ll4rrr", "foll_r", "f0ll_r",
    "f0ll4_r", "f0l1arX", "f0ll4r-test",
    "f0ll4r.mock", "f0ll4r.fake", "f0ll4r.sim",
    "f0ll4r-obf", "f0ll4r-enc",

    # --- Necrofilia / variantes ---
    "necrofilia", "necrofília", "necrofilo", "necrófilo",
    "necrofil@", "n3crofilia", "necr0filia",
    "necro-philia", "necr0f1lia", "necro_filia",

    # --- Sexo / variantes ---
    "sexo", "s3xo", "sex0", "seWo", "s€xo",
    "sx", "sxo", "sexo+", "sexo!", "sexo?",
    "sex@", "se_xo",

    # --- Mierda / variantes ---
    "mierda", "m13rda", "mi3rda", "mierd@", "mierd4",
    "m!erda", "mier-da", "mierda!", "mierda?",
    "mrd", "m1erda","mierdon","mierdón",

    # --- Ñordo / variantes ---
    "ñordo", "nordo", "ñ0rdo", "n0rdo",
    "ñord@", "nord@", "ñ0rd0", "n0rd0",
    "ñordo!", "ñordo?",
    "caca", "kaka", "k4ka",
    "culo", "cul0",
    "pedazo de mierda", "mierdecilla",
    "cagar", "cagada", "cagón",
    "cag4r", "c4gada",

    # --- Insultos sexuales / variantes ---
    "cabrona", "cabrón", "c4brona", "c4brón",
    "putain", "put4in",
    "puta", "put@", "put4",
    "puto", "put0",
    "zorra", "z0rra",
    "perra",
    "prostituta", "prostitución",
    "masturbar", "masturbación", "paja",
    "pajear", "paj3ar",
    "corrida", "correrse",
    "orgasmo", "orgasm0",

    # --- Violencia / variantes ---
    "asesinar", "asesinato",
    "matar", "m4tar",
    "asesinar", "asesino",
    "violento", "violencia",
    "apuñalar", "apuñalamiento",
    "disparar", "tiroteo",
    "secuestrar", "secuestro",
    "tortura", "torturar",

    # --- Drogas / variantes ---
    "metanfetamina", "meta", "meth",
    "cocaína", "cocaina", "coc4ina",
    "heroína", "heroina",
    "porro", "porros",
    "marihuana", "maría",
    "hachís", "hachis",
    "droga", "drogas",
    "yonki", "yonqui",

    # --- MAsturbacion ---
    "masturbación", "masturbacion", "masturbarse",
    "masturbe", "masturbate", "masturbate!","paja","pajearse",
    "pajero","pajera","pajilla","pajote",
    "pajilla","pajillero","pajillera",
    "pajillero","pajillera",
    "pajillero","pajillera",

    # --- palabrotas ---
    "gilipollas", "g1lipollas", "gil1pollas",
    "imbecil", "imbécil", "1mbecil",
    "idiota", "1diota",
    "subnormal", "subnorm4l",
    "estupido", "estúpido",
    "retrasado", "retr4sado",
    "asqueroso", "asqueros@",
    "basura", "basur4",
    "escoria","cabron",


    # --- Política / variantes ---
    "ayuso","pedro sanchez","sanchez","psoe","pp","vox","podemos",
    "izquierda unida","ciudadanos","partido popular","partido socialista","extrema derecha","extrema izquierda",
    "socialismo","comunismo","fascismo","dictadura","democracia", "liberalismo","conservadurismo",
]

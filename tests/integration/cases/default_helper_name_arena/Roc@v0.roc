module [arena]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

arena : Val
arena = RDict [
    ("a", RInt 1i128),
]

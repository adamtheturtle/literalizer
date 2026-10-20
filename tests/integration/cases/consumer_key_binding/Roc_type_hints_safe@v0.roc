module [key_binding]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

key_binding : Val
key_binding = RDict [
    ("a", RInt 1i128),
]

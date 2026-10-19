module [k]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

k : Val
k = RDict [
    ("a", RInt 1i128),
]

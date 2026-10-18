module [my_data]

Val : [
    RNull,
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

actual : Val
actual = RDict [
    ("_", RStr "_"),
]
my_data : Val
my_data = RList [
    RDict [("$ref", RInt 1i128)],
    RDict [("$ref", RNull)],
    actual,
]

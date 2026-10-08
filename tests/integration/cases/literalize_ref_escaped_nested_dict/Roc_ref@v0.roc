module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

existing : Val
existing = RInt 1i128
my_data : Val
my_data = RDict [
    ("nested", RList [RInt 0i128, existing]),
]

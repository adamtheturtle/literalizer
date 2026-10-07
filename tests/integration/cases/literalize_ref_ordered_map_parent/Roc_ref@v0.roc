module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

bound : Val
bound = RInt 2i128
my_data : Val
my_data = RDict [
    ("value", bound),
]

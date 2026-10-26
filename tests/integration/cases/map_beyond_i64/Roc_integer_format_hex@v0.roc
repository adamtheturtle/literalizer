module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RInt 0x7fffffffffffffffi128),
    ("b", RInt 0x8000000000000000i128),
]

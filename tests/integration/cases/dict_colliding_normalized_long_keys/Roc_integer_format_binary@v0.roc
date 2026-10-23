module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a_b", RInt 0b1i128),
    ("a-b", RInt 0b10i128),
    ("averyveryverylongkeynamethatgoesonandonandon", RInt 0b11i128),
    ("averyveryverylongkeynamethatgoesonandmore", RInt 0b100i128),
]

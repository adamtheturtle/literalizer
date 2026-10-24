module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a_b", RInt 0o1i128),
    ("a-b", RInt 0o2i128),
    ("averyveryverylongkeynamethatgoesonandonandon", RInt 0o3i128),
    ("averyveryverylongkeynamethatgoesonandmore", RInt 0o4i128),
]

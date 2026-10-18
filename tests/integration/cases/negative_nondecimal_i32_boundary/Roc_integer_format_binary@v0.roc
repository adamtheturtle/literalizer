module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("minimum", RInt -0b10000000000000000000000000000000i128),
    ("below", RInt -0b10110010110100000101111000000000i128),
]

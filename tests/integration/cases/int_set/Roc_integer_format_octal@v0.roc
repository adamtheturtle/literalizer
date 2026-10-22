module [my_data]

Val : [
    RInt I128,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RInt 0o1i128,
    RInt 0o2i128,
    RInt 0o3i128,
]

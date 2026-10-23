module [my_data]

Val : [
    RInt I128,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RInt 0o1i128,
    RInt 0o20000000000000i128,
]

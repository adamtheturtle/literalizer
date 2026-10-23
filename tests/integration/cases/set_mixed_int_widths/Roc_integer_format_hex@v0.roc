module [my_data]

Val : [
    RInt I128,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RInt 0x1i128,
    RInt 0x10000000000i128,
]

module [my_data]

Val : [
    RInt I128,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RInt 0b1i128,
    RInt 0b10000000000000000000000000000000000000000i128,
]

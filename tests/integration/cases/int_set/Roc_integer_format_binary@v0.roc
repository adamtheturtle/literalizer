module [my_data]

Val : [
    RInt I128,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RInt 0b1i128,
    RInt 0b10i128,
    RInt 0b11i128,
]

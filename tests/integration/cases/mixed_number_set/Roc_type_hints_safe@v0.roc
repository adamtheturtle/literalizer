module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RFloat 2.5,
    RInt 1i128,
]

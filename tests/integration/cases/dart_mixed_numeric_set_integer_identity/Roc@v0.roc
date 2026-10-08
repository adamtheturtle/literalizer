module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RFloat 1.5,
    RInt 9007199254740993i128,
]

module [my_data]

Val : [
    RInt I128,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RInt 10i128,  # comment for ten
    RInt 2i128,  # comment for two
]

module [my_data]

Val : [
    RInt I128,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RInt 1i128,
    RInt 2i128,
    RInt 3i128,
    ]

module [my_data]

Val : [
    RInt I128,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RInt 1i128,
    RInt 1099511627776i128,
    ]

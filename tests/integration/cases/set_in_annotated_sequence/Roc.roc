module [my_data]

Val : [
    RInt I128,
    RList (List Val),
    RSet (List Val),
]

my_data : Val
my_data = RList [
    RSet [],
    RSet [RInt 1i128, RInt 2i128],
    RList [],
    ]

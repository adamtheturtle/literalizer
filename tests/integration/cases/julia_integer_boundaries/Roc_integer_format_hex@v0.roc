module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt -0x8000000000000000i128,
    RInt 0x8000000000000000i128,
    ]

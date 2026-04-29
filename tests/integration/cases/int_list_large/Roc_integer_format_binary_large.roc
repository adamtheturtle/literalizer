module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0b11110100001001000000i128,
    RInt -0b10011010010i128,
    RInt 0b11111111i128,
    RInt -0b1010i128,
    ]

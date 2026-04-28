module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0b11110100001001000000,
    RInt -0b10011010010,
    RInt 0b11111111,
    RInt -0b1010,
    ]

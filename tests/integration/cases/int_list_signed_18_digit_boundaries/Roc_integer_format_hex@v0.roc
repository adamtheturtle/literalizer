module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0xde0b6b3a763ffffi128,
    RInt -0xde0b6b3a763ffffi128,
]

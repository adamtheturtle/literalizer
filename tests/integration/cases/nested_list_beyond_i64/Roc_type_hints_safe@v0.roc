module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RInt 1i128],
    RList [RInt 1180591620717411303424i128],
]

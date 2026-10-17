module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

existing : Val
existing = RInt 1i128
my_data : Val
my_data = RList [
    RInt 0i128,
    RList [RList [existing]],
]

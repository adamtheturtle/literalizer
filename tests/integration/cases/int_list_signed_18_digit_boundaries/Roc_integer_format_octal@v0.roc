module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0o67405553164730777777i128,
    RInt -0o67405553164730777777i128,
]

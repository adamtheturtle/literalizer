module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

ref_x : Val
ref_x = RInt 3i128
my_data : Val
my_data = RList [
    ref_x,
    RInt 1i128,
    RInt 2i128,
    ]

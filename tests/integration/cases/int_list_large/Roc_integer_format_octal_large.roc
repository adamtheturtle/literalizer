module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0o3641100i128,
    RInt -0o2322i128,
    RInt 0o377i128,
    RInt -0o12i128,
    ]

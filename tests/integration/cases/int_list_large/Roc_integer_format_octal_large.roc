module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0o3641100,
    RInt -0o2322,
    RInt 0o377,
    RInt -0o12,
    ]

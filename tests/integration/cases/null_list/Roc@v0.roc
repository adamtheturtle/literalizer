module [my_data]

Val : [
    RNull,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RNull,
    RNull,
    ]

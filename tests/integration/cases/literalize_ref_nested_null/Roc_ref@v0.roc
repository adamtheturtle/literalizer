module [my_data]

Val : [
    RNull,
    RList (List Val),
]

my_null : Val
my_null = RNull
my_data : Val
my_data = RList [
    my_null,
    RNull,
]

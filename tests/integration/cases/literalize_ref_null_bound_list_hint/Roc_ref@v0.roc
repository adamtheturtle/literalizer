module [my_data]

Val : [
    RNull,
    RInt I128,
    RList (List Val),
]

my_value : Val
my_value = RNull
my_data : Val
my_data = my_value

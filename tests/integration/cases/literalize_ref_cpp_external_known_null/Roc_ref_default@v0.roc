module [main]

Val : [
    RNull,
]

item : Val
item = RNull
my_data : Val
my_data = RNull
main =
    dbg ((void)my_data;)
    dbg (my_data = item)
    dbg ((void)my_data;)
    {}

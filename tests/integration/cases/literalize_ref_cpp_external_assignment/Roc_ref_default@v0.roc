module [main]

Val : [
    RInt I128,
    RList (List Val),
]

ref_data : Val
ref_data = RList [
    RInt 1i128,
    RInt 2i128,
]
my_data : Val
my_data = RList [
    RInt 0i128,
]
main =
    dbg ((void)my_data;)
    dbg (my_data = ref_data)
    dbg ((void)my_data;)
    {}

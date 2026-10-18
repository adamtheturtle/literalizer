module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("nested", RDict [("times", RList [RInt -2208988800i128])])],
    RDict [],
]

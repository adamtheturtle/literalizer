module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RList [RDict [("values", RList [RList []])], RDict []],
    RList [RDict [], RDict [("values", RList [RList []])]],
]

module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("items", RList [RDict [("inner", RDict [("x", RInt 1i128)])], RDict [("inner", RDict [])]])],
    RDict [("items", RList [RDict [("inner", RDict [("x", RInt 2i128)])], RDict [("inner", RDict [])]])],
]

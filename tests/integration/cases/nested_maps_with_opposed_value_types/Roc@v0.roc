module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("input", RDict [("name", RStr "alice"), ("city", RStr "paris")]), ("expected", RDict [("count", RInt 1i128), ("total", RInt 2i128)])],
    RDict [("input", RDict [("name", RInt 10i128), ("city", RInt 20i128)]), ("expected", RDict [("count", RStr "done"), ("total", RStr "pending")])],
]

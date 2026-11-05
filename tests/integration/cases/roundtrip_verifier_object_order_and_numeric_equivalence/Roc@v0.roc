module [my_data]

Val : [
    RNull,
    RBool Bool,
    RFloat F64,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("b", RNull),
    ("a", RDict [("y", RList [RFloat 1.0]), ("x", RBool Bool.false)]),
]

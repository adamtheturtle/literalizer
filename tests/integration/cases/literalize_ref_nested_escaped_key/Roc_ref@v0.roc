module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

foo : Val
foo = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = RDict [
    ("mapping", RDict [("value", foo)]),
    ("items", RList [RDict [("other", RInt 1i128)], foo]),
    ]

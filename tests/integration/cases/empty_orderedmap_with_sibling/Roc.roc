module [my_data]

Val : [
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [],
    RList [],
    ]

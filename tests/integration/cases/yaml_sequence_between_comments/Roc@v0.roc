module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("item", RStr "existing")],
    # This comment describes the next item.
    RDict [("item", RStr "next")],
    ]

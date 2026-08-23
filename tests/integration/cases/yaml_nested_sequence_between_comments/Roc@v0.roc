module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RList [
        RDict [("item", RStr "existing")],
        RStr "kept",
        # This comment trails the first pair.
        ],
    RList [RDict [("item", RStr "next")], RStr "also kept"],
    # This comment describes the last pair.
    RList [RDict [("item", RStr "last")], RStr "kept too"],
    ]

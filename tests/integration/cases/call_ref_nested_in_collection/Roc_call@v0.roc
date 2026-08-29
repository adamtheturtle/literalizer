module [main]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]
process : a, b -> {}
process = \_, _ -> {}

big_list : Val
big_list = RList [
    RStr "x",
    ]
main =
    dbg (process (RDict [("k", big_list)]) (RInt 2i128))
    {}

module [main]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]
process : a -> {}
process = \_ -> {}

big_list : Val
big_list = RList [
    RStr "x",
    ]
main =
    dbg (process (RDict [("m", big_list)]))
    {}

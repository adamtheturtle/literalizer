module [main]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]
process : a -> {}
process = \_ -> {}

my_list : Val
my_list = RDict [
    ("unused", RStr "value"),
    ]
main =
    dbg (process (RList [RList [RDict [("inner", my_list)]]]))
    {}

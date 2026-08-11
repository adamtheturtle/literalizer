module [main]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]
consume : a, b -> {}
consume = \_, _ -> {}

foo : Val
foo = RInt 42i128
main =
    dbg (consume (RList [)
    dbg (    RDict [)
    dbg (        ("other", RInt 1i128),)
    dbg (        ],)
    dbg (    foo,)
    dbg (    ]) (RDict [)
    dbg (    ("left", foo),)
    dbg (    ("other", RInt 1i128),)
    dbg (    ]))
    {}

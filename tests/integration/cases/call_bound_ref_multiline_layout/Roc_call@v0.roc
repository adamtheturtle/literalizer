module [main]

Val : [
    RInt I128,
    RList (List Val),
]
f : a -> {}
f = \_ -> {}

x : Val
x = RList [
    RList [
        RInt 1i128,
        RInt 2i128,
    ],
    RList [
        RInt 3i128,
        RInt 4i128,
    ],
]
main =
    dbg (f (RList [
        RList [
            x,
        ],
    ]))
    {}

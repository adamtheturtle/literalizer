module [main]

Val : [
    RInt I128,
    RList (List Val),
]
f : a -> {}
f = \_ -> {}

ref_data : Val
ref_data = RList [
    RInt 1i128,
    RInt 2i128,
]
main =
    dbg (f (RList [
        ref_data,
    ]))
    dbg (f (RList [
        ref_data,
    ]))
    {}

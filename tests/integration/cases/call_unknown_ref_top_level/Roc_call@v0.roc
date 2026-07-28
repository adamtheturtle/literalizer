module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

unknown_value : Val
unknown_value = RList [
    RInt 1i128,
    ]
main =
    dbg (process unknown_value)
    {}

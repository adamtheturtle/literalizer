module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

known_value : Val
known_value = RInt 1i128
unknown_value : Val
unknown_value = RList []
main =
    dbg (process unknown_value)
    {}

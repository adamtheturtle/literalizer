module [main]

Val : [
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

unknown_value : Val
unknown_value = RList []
main =
    dbg (process unknown_value)
    {}

module [main]

Val : [
    RInt I128,
]
process : a -> {}
process = \_ -> {}

value : Val
value = RInt 1i128
main =
    dbg (process value)
    {}

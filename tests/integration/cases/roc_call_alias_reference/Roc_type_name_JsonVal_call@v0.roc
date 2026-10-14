module [main]

JsonVal : [
    RInt I128,
]
process : a -> {}
process = \_ -> {}

value : JsonVal
value = RInt 1i128
main =
    dbg (process value)
    {}

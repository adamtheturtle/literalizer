module [main]

Val : [
    RInt I128,
    RList (List Val),
]
send : a -> {}
send = \_ -> {}

existing : Val
existing = RInt 42i128
main =
    dbg (send existing)
    {}

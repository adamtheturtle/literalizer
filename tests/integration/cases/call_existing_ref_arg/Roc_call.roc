module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

existing : Val
existing = RInt 42i128
main =
    dbg (process existing)
    {}

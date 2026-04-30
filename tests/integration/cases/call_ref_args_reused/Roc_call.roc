module [main]

Val : [
    RInt I128,
    RList (List Val),
]
process : a, b -> {}
process = \_, _ -> {}

shared : Val
shared = RInt 1i128
other : Val
other = RInt 2i128
main =
    dbg (process shared (RInt 1i128))
    dbg (process other (RInt 0i128))
    dbg (process shared (RInt 8i128))
    {}

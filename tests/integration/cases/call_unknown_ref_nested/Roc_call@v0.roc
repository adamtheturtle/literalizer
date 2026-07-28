module [main]

Val : [
    RBool Bool,
    RList (List Val),
]
process : a, b -> {}
process = \_, _ -> {}

known_value : Val
known_value = RBool Bool.true
unknown_value : Val
unknown_value = RBool Bool.true
main =
    dbg (process known_value unknown_value)
    {}

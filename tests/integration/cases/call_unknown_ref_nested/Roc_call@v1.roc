Val := [
    RBool(Bool),
    RList(List(Val)),
]
process = |_, _| {}

known_value : Val
known_value = RBool(Bool.True)
unknown_value : Val
unknown_value = RBool(Bool.True)

main! = |_args| {
    dbg (process(known_value, unknown_value))
    Ok({})
}

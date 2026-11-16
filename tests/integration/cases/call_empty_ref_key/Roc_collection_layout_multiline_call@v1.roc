Val := [
    RInt(I128),
    RList(List(Val)),
]
consume = |_| {}

external_value : Val
external_value = RInt(1.I128)

main! = |_args| {
    dbg (consume(external_value))
    Ok({})
}

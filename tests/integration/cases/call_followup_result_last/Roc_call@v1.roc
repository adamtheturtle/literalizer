Val := [
    RInt(I128),
    RList(List(Val)),
]
make_widget = |_, _| {}
consume = |_, _| {}

my_data = make_widget(RInt(42.I128), RInt(3.I128))

main! = |_args| {
    dbg (consume(RInt(3.I128), my_data))
    Ok({})
}

Val := [
    RInt(I128),
]
make_widget = |_| {}

value : Val
value = RInt(1.I128)

main! = |_args| {
    dbg (make_widget(value))
    Ok({})
}

Val := [
    RList(List(Val)),
]
make_widget = |_| {}

items : Val
items = RList([])

main! = |_args| {
    dbg (make_widget(items))
    Ok({})
}

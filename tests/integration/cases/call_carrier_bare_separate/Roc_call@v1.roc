make_widget = |_, _| {}



main! = |_args| {
    dbg (make_widget(RList([RInt(1.I128)]), RList([RStr("text")])))
    Ok({})
}

make_widget = |_, _| {}



main! = |_args| {
    dbg (make_widget(RList([RInt(1.I128)]), RList([RInt(2.I128)])))
    Ok({})
}

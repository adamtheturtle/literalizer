make_widget = |_, _, _| {}



main! = |_args| {
    dbg (make_widget(RList([]), RList([RInt(1.I128)]), RList([])))
    dbg (make_widget(RList([RStr("text")]), RList([RInt(2.I128)]), RList([])))
    dbg (make_widget(RList([]), RList([RStr("text")]), RList([])))
    dbg (make_widget(RList([RStr("text")]), RList([RInt(2.I128)]), RList([RInt(3.I128)])))
    Ok({})
}

consume_widget = |_| {}



main! = |_args| {
    dbg (consume_widget(RSet([
        RInt(1.I128),
        RInt(2.I128),
    ])))
    Ok({})
}

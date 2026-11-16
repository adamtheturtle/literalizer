make_widget = |_| {}



main! = |_args| {
    dbg (make_widget(RInt(1.I128)))
    Ok({})
}

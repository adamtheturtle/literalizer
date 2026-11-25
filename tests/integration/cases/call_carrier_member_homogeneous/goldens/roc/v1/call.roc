app_go = |_, _| {}



main! = |_args| {
    dbg (app_go(RList([RInt(1.I128)]), RList([RInt(2.I128)])))
    Ok({})
}

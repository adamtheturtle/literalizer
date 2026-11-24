thing_first_value = |_| {}



main! = |_args| {
    dbg (thing_first_value(RInt(1.I128)))
    Ok({})
}

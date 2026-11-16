obj_class = |_| {}



main! = |_args| {
    dbg (obj_class(RInt(42.I128)))
    Ok({})
}

check_wrapper = |_| {}



main! = |_args| {
    dbg (check_wrapper(RInt(42.I128)))
    Ok({})
}

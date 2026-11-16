do_thing = |_| {}



main! = |_args| {
    dbg (do_thing(RInt(1.I128)))
    dbg (do_thing(RInt(2.I128)))
    Ok({})
}

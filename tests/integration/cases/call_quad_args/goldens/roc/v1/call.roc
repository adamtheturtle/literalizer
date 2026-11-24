process = |_, _, _, _| {}



main! = |_args| {
    dbg (process(RInt(1.I128), RInt(2.I128), RInt(3.I128), RInt(4.I128)))
    dbg (process(RInt(5.I128), RInt(6.I128), RInt(7.I128), RInt(8.I128)))
    Ok({})
}

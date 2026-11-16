thing_go = |_, _, _| {}



main! = |_args| {
    dbg (thing_go(RList([]), RList([RInt(1.I128)]), RList([])))
    dbg (thing_go(RList([RStr("text")]), RList([RInt(2.I128)]), RList([])))
    dbg (thing_go(RList([]), RList([RStr("text")]), RList([])))
    dbg (thing_go(RList([RStr("text")]), RList([RInt(2.I128)]), RList([RInt(3.I128)])))
    Ok({})
}

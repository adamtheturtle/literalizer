consume = |_, _, _| {}



main! = |_args| {
    dbg (consume({ x: 1.I128 }, 2.I128, "first"))
    dbg (consume({ name: "Ada" }, 3.I128, "second"))
    Ok({})
}

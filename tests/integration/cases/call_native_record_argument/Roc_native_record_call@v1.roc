consume = |_| {}



main! = |_args| {
    dbg (consume({ x: 1.I128 }))
    Ok({})
}

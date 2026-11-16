consume = |_| {}



main! = |_args| {
    dbg (consume({ name: "Ada" }))
    Ok({})
}

process = |_| {}



main! = |_args| {
    dbg (process(RStr("time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)")))
    Ok({})
}

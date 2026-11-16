api_process = |_| {}



main! = |_args| {
    dbg (api_process(RDict([])))
    Ok({})
}

api_worker_process = |_, _| {}



main! = |_args| {
    dbg (api_worker_process(RList([RInt(1.I128), RDict([])]), RInt(42.I128)))
    dbg (api_worker_process(RList([RInt(2.I128), RDict([("x", RStr("s"))])]), RInt(43.I128)))
    Ok({})
}

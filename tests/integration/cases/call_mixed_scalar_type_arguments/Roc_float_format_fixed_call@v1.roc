capture = |_, _, _, _, _, _, _| {}



main! = |_args| {
    dbg (capture(RFloat(F64.nan), RFloat(F64.infinity), RFloat(-F64.infinity), RFloat(1.250000.F64), RStr("2024-01-15"), RStr("2024-01-15T12:34:56"), RStr("[ordinary text]")))
    Ok({})
}

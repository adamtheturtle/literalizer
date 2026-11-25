capture = |_, _, _, _, _, _, _| {}



main! = |_args| {
    dbg (capture(RFloat(F64.nan), RFloat(F64.infinity), RFloat(-F64.infinity), RFloat(1.25.F64), RStr("2024-01-15"), RInt(1705322096.I128), RStr("[ordinary text]")))
    Ok({})
}

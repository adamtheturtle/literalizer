throttler_check = |_, _| {}
emit = |_| {}



main! = |_args| {
    dbg (emit(throttler_check(RStr("user_1"), RFloat(1000.0.F64))))
    dbg (emit(throttler_check(RStr("user_2"), RFloat(2000.5.F64))))
    Ok({})
}

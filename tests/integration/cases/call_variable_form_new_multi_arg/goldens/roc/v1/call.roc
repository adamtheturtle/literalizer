record_entry = |_, _, _| {}

my_data = record_entry(RStr("a"), RInt(1.I128), RBool(Bool.True))

main! = |_args| {
    _ = my_data
    Ok({})
}

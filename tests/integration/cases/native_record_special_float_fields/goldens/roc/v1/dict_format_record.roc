my_data = {
    positive: F64.infinity,
    negative: -F64.infinity,
    nan_value: F64.nan,
    finite: 1.5.F64,
}

main! = |_args| {
    _ = my_data
    Ok({})
}

my_data = {
    minimum: -2147483648.I128,
    neighbor: -2147483647.I128,
    maximum: 2147483647.I128,
    nested: [
        -2147483648.I128,
    ],
}

main! = |_args| {
    _ = my_data
    Ok({})
}

my_data = {
    outer: {
        a: 1.I128,
        b: "x",
        c: RNull,
    },
}

main! = |_args| {
    _ = my_data
    Ok({})
}

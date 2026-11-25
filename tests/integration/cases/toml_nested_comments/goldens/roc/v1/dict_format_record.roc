my_data = {
    dotted: {
        first: 1.I128,
        second: 2.I128,
    },
    plain: 3.I128,
    entries: [
        {
            name: "one",
        },
        {
            name: "two",
        },
    ],
    table: {
        inner: 4.I128,
    },
}

main! = |_args| {
    _ = my_data
    Ok({})
}

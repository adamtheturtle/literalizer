my_data = {
    owner: {
        name: "Ada",
        active: Bool.False,
    },
    members: [
        {
            name: "Ada",
            score: 1.5.F64,
        },
        {
            name: "Bob",
            score: 2.5.F64,
        },
    ],
}

main! = |_args| {
    _ = my_data
    Ok({})
}

my_data = [
    { name: "Ada", active: Bool.True, count: 1.I128, score: 1.5.F64, missing: RNull, scores: [1.I128, 2.I128], child: { age: 3.I128 } },
    { name: "Bob", active: Bool.False, count: 2.I128, score: 2.5.F64, missing: RNull, scores: [4.I128], child: { age: 5.I128 } },
]

main! = |_args| {
    _ = my_data
    Ok({})
}

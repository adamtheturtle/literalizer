Val := [
    RInt(I128),
]

first_value : Val
first_value = RInt(1.I128)

main! = |_args| {
    _ = first_value
    Ok({})
}

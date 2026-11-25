Val := [
    RInt(I128),
]

i12345 : Val
i12345 = RInt(1.I128)

main! = |_args| {
    _ = i12345
    Ok({})
}

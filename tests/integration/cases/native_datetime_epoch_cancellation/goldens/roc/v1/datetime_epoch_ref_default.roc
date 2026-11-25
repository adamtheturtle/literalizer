Val := [
    RInt(I128),
]

stamp : Val
stamp = RInt(0.I128)
result_data : Val
result_data = stamp

main! = |_args| {
    _ = result_data
    Ok({})
}

Val := [
    RInt(I128),
    RList(List(Val)),
]
f = |_| {}
repr = |_| {}

ref_data : Val
ref_data = RInt(1.I128)

main! = |_args| {
    dbg (repr(f(ref_data)))
    Ok({})
}

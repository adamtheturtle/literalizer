Val := [
    RInt(I128),
    RList(List(Val)),
]
f = |_| {}

ref_data : Val
ref_data = RList([
    RList([
        RInt(1.I128),
        RInt(2.I128),
    ]),
    RList([
        RInt(3.I128),
        RInt(4.I128),
    ]),
])

main! = |_args| {
    dbg (f(RList([
        RList([
            ref_data,
        ]),
    ])))
    Ok({})
}

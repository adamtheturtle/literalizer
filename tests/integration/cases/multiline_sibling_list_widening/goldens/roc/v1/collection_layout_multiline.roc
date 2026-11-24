Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("omap_value", RDict([
        ("first", RInt(1.I128)),
    ])),
    ("sibling_lists", RDict([
        ("numbers", RList([
            RInt(1.I128),
            RInt(2.I128),
        ])),
        ("strings", RList([
            RStr("x"),
            RStr("y"),
        ])),
    ])),
    ("ref_marker_present", RList([
        RStr("$keep"),
        RStr("z"),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}

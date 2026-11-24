Val := [
    RNull,
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # null heading
    # before null
    ("a", RNull),  # first null
    ("b", RNull),  # second null
])

main! = |_args| {
    _ = my_data
    Ok({})
}

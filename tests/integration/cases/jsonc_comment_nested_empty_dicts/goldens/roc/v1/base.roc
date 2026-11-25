Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # outer heading
    # first empty
    ("a", RDict([])),
    # second empty
    ("b", RDict([])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}

Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("first", RList([RInt(1.I128), RInt(2.I128)])),
    ("second", RInt(3.I128)),  # About the second key.
])

main! = |_args| {
    _ = my_data
    Ok({})
}

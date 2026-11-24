Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # A JSONC input case with both comment forms.
    ("url", RStr("https://example.org/a/*b*/")),  # detail
    # continued
    ("count", RInt(0o2.I128)),  # trailing line comment
])

main! = |_args| {
    _ = my_data
    Ok({})
}

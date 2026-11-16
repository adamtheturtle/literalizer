Val := [
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # Server configuration
    ("host", RStr("localhost")),  # default host
    ("port", RInt(8080.I128)),
    # Enable debug mode
    ("debug", RBool(Bool.True)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}

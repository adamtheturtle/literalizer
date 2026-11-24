Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("v", RStr("a\u(00ad)\u(200b)\u(200d)\u(200e)\u(202e)\u(2060)\u(feff)\u(2028)\u(2029)b")),
    ("a\u(00ad)\u(200b)\u(200d)\u(200e)\u(202e)\u(2060)\u(feff)\u(2028)\u(2029)b", RInt(1.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}

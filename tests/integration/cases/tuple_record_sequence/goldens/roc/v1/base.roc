Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("call", RStr("send")), ("args", RList([RInt(1.I128), RStr("email"), RStr("a@gmail.com"), RInt(100.I128)]))]),
    RDict([("call", RStr("recv")), ("args", RList([RInt(2.I128), RStr("sms"), RStr("b@example.com"), RInt(200.I128)]))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}

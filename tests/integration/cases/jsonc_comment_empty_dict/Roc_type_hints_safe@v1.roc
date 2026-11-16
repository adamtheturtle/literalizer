Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

# empty heading
# empty body
# after empty
my_data : Val
my_data = RDict([])

main! = |_args| {
    _ = my_data
    Ok({})
}

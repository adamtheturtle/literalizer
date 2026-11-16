Val := [
    RList(List(Val)),
]

# empty heading
# empty body
# after empty
my_data : Val
my_data = RList([])

main! = |_args| {
    _ = my_data
    Ok({})
}

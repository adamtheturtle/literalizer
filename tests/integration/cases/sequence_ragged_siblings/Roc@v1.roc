Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RStr("set_task"), RStr("web"), RStr("lint_web")]),
    RList([RStr("merge_pipelines")]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}

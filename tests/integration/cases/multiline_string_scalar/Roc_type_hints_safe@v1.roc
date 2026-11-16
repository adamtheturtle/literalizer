Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("\nroot first line\n  indented\n\nroot last line\n")

main! = |_args| {
    _ = my_data
    Ok({})
}

module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "中中中中中中中中中中中中中中中中中中中中",
    RStr "é'é'é'é'é'é'é'é'é'é'",
    RStr "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂",
]

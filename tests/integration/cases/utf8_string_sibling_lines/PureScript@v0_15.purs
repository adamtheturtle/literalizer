module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "中中中中中中中中中中中中中中中中中中中中",
    PStr "é'é'é'é'é'é'é'é'é'é'",
    PStr "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
]

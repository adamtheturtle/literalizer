module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "中中中中中中中中中中中中中中中中中中中中",
    EStr "é'é'é'é'é'é'é'é'é'é'",
    EStr "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
    ]

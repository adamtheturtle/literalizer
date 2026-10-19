module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "中中中中中中中中中中中中中中中中中中中中";
    FStr "é'é'é'é'é'é'é'é'é'é'";
    FStr "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
]

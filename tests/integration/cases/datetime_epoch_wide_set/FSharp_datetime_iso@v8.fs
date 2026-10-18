module Main

type Val =
    | FSet of Val list
    | FStr of string
let my_data: Val = FSet [
    FStr "2099-06-15T08:30:00"
]

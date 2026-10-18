module Main

type Val =
    | FSet of Val list
    | FStr of string
let my_data: Val = FSet [
    FStr "1969-12-31T23:59:59+00:00"
]

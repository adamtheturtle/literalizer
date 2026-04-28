module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "prefix ${HOME} suffix";
    FStr "${interpolated}"
]

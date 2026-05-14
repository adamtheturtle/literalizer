module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "line1\r\nline2";
    FStr "line1\rline2";
    FStr ""
]

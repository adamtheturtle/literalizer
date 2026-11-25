module Main

type Val =
    | FList of Val list
    | FStr of string
let my_data: Val = FList [
    FStr "1901-12-13T20:45:51";
    FStr "1901-12-13T20:45:52";
    FStr "2038-01-19T03:14:07";
    FStr "2038-01-19T03:14:08"
]

module Main

type Val =
    | FList of Val list
    | FStr of string
let my_data: Val = FList [
    FStr "1970-01-01T00:00:00.000001+00:00";
    FStr "1969-12-31T23:59:59.500000+00:00";
    FStr "1970-01-01T00:00:01+00:00"
]

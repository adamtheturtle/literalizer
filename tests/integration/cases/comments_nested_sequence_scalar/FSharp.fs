module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FList [FStr "ADD"; FStr "alice"; FStr "hello"];
    FList [FStr "DEL"; FStr "bob"; FStr "5"]  // removes "world"
]

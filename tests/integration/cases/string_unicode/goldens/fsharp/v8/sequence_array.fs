module Main

type Val =
    | FStr of string
    | FList of Val array
let my_data: Val array = [|
    FStr "café";
    FStr "中文";
    FStr "😀"
|]

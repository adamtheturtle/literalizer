module Main

type Val =
    | FStr of string
    | FList of Val array
let my_data: Val array = [|
    FStr "48656c6c6f"
|]

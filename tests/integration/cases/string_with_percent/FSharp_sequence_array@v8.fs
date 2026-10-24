module Main

type Val =
    | FStr of string
    | FList of Val array
let my_data: Val array = [|
    FStr "100% done";
    FStr "%(name) is here"
|]

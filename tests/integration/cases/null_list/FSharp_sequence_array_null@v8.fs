module Main

type Val =
    | FNull
    | FList of Val list
let my_data: Val array = [|
    FNull;
    FNull
|]

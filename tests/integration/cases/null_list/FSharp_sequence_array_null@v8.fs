module Main

type Val =
    | FNull
    | FList of Val array
let my_data: Val array = [|
    FNull;
    FNull
|]

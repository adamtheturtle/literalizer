module Main

type Val =
    | FList of Val list
let shared: Val array = [||]
let my_data: Val array = [|
    shared;
    shared
|]

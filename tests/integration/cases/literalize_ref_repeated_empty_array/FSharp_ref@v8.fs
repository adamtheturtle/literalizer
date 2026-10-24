module Main

type Val =
    | FList of Val array
let shared: Val array = [||]
let my_data: Val array = [|
    FList (shared);
    FList (shared)
|]

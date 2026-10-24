module Main

type Val =
    | FList of Val array
let my_data: Val array = [|
    FList ([|FList ([||])|]);
    FList ([|FList ([||])|])
|]

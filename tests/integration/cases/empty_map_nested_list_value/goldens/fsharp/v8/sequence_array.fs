module Main

type Val =
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
let my_data: Val array = [|
    FList ([|FMap [("values", FList ([|FList ([||])|]))]; FMap []|]);
    FList ([|FMap []; FMap [("values", FList ([|FList ([||])|]))]|])
|]

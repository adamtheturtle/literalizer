module Main

type Val =
    | FInt of int64
    | FList of Val array
let my_data: Val array = [|
    FList ([|FList ([||]); FList ([||])|]);
    FList ([|FList ([|FInt 1L|]); FList ([|FInt 1L|])|])
|]

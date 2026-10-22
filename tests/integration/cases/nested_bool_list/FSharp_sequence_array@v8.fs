module Main

type Val =
    | FBool of bool
    | FList of Val array
let my_data: Val array = [|
    FList ([|FBool true; FBool false|]);
    FList ([|FBool true; FBool true|])
|]

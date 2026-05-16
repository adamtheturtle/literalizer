module Main

type Val =
    | FBool of bool
    | FList of Val list
let my_data: Val array = [|
    FBool true;
    FBool false;
    FBool true
|]

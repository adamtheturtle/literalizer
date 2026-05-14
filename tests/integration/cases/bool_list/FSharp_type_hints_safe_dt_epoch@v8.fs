module Main

type Val =
    | FBool of bool
    | FList of Val list
let my_data: Val = FList [
    FBool true;
    FBool false;
    FBool true
]

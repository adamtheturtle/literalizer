module Main

type Val =
    | FBool of bool
    | FList of Val list
let my_data: Val = FList [
    FList [FBool true; FBool false];
    FList [FBool true; FBool true]
]

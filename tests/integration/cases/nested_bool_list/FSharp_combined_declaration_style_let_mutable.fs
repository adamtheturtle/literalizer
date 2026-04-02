module Check

type Val =
    | FBool of bool
    | FList of Val list
let mutable my_data: Val = FList [
    FList [FBool true; FBool false];
    FList [FBool true; FBool true]
]

module Check

type Val =
    | FBool of bool
    | FList of Val list
let mutable my_data: Val = FList [
    FBool true;
    FBool false;
    FBool true
]

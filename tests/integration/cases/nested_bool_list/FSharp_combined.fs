module Check

type Val =
    | FBool of bool
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FList [FBool true; FBool false];
        FList [FBool true; FBool true]
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FList [FBool true; FBool false];
        FList [FBool true; FBool true]
    ]
    ignore my_data

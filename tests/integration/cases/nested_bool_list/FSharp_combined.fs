module Main

type Val =
    | FBool of bool
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FList [FBool true; FBool false];
        FList [FBool true; FBool true]
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FList [FBool true; FBool false];
        FList [FBool true; FBool true]
    ]
    ignore my_data

module Main

type Val =
    | FInt of int64
    | FList of Val list
    | FSet of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FSet [];
        FSet [FInt 1L; FInt 2L];
        FList []
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FSet [];
        FSet [FInt 1L; FInt 2L];
        FList []
    ]
    ignore my_data

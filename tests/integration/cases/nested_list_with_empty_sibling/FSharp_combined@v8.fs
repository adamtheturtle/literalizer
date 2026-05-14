module Main

type Val =
    | FInt of int64
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FList [FInt 1L; FInt 2L];
        FList [];
        FList [FInt 3L; FInt 4L]
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FList [FInt 1L; FInt 2L];
        FList [];
        FList [FInt 3L; FInt 4L]
    ]
    ignore my_data

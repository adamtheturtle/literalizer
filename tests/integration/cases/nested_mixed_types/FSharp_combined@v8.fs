module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FList [FInt 1L; FInt 2L];
        FList [FStr "a"; FStr "b"]
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FList [FInt 1L; FInt 2L];
        FList [FStr "a"; FStr "b"]
    ]
    ignore my_data

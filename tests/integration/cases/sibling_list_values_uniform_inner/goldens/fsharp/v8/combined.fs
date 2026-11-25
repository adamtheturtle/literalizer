module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("lint", FList [FInt 2L; FList [FInt 1L]]);
        ("test", FList [FInt 5L; FList [FInt 7L]])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("lint", FList [FInt 2L; FList [FInt 1L]]);
        ("test", FList [FInt 5L; FList [FInt 7L]])
    ]
    ignore my_data

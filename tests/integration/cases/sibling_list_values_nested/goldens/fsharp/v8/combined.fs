module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("lint", FList [FInt 2L; FList []]);
        ("test", FList [FInt 5L; FList [FStr "compile"]])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("lint", FList [FInt 2L; FList []]);
        ("test", FList [FInt 5L; FList [FStr "compile"]])
    ]
    ignore my_data

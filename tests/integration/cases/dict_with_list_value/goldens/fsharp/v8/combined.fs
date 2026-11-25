module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("name", FStr "Alice");
        ("scores", FList [FInt 10L; FInt 20L; FInt 30L])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("name", FStr "Alice");
        ("scores", FList [FInt 10L; FInt 20L; FInt 30L])
    ]
    ignore my_data

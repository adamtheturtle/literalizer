module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FList [FList [FMap [("$ref", FStr "myVar")]; FInt 42L; FStr "static"]]
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FList [FList [FMap [("$ref", FStr "myVar")]; FInt 42L; FStr "static"]]
    ]
    ignore my_data

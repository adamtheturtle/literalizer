module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
    | FSet of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("name", FStr "Alice");
        ("tags", FSet [FBool true; FInt 42L; FStr "apple"])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("name", FStr "Alice");
        ("tags", FSet [FBool true; FInt 42L; FStr "apple"])
    ]
    ignore my_data

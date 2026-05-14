module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("metrics", FMap [("count", FInt 100L); ("rate", FInt 50L)]);
        ("flags", FMap [("retries", FInt 3L); ("timeout", FInt 30L)])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("metrics", FMap [("count", FInt 100L); ("rate", FInt 50L)]);
        ("flags", FMap [("retries", FInt 3L); ("timeout", FInt 30L)])
    ]
    ignore my_data

module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("id", FInt 1L);
        ("owner", FMap [("name", FStr "Alice"); ("age", FInt 30L)])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("id", FInt 1L);
        ("owner", FMap [("name", FStr "Alice"); ("age", FInt 30L)])
    ]
    ignore my_data

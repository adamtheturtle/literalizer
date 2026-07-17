module Main

type Val =
    | FInt of bigint
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("a", FInt 9223372036854775807L);
        ("b", FInt 9223372036854775808I)
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("a", FInt 9223372036854775807L);
        ("b", FInt 9223372036854775808I)
    ]
    ignore my_data

module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("name", FStr "Alice");
        ("age", FInt 30L);
        ("active", FBool true);
        ("score", FFloat 4.5)
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("name", FStr "Alice");
        ("age", FInt 30L);
        ("active", FBool true);
        ("score", FFloat 4.5)
    ]
    ignore my_data

module Main

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
    | FDate of System.DateTime
    | FDatetime of System.DateTime
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("name", FStr "Alice");
        ("age", FInt 30L);
        ("active", FBool true);
        ("score", FNull);
        ("joined", FStr (string (System.DateOnly(2024, 1, 15))));
        ("last_login", FStr (string (System.DateTime(2024, 1, 15, 12, 30, 0))));
        ("avatar", FStr "48656c6c6f")
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("name", FStr "Alice");
        ("age", FInt 30L);
        ("active", FBool true);
        ("score", FNull);
        ("joined", FStr (string (System.DateOnly(2024, 1, 15))));
        ("last_login", FStr (string (System.DateTime(2024, 1, 15, 12, 30, 0))));
        ("avatar", FStr "48656c6c6f")
    ]
    ignore my_data

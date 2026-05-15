module Main

type Val =
    | FBool of bool
    | FInt of bigint
    | FFloat of float
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("quantity", FInt 1000000L);
        ("big", FInt 18446744073709551615I);
        ("ratio", FFloat 2.5);
        ("label", FStr "tag");
        ("ok", FBool true)
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("quantity", FInt 1000000L);
        ("big", FInt 18446744073709551615I);
        ("ratio", FFloat 2.5);
        ("label", FStr "tag");
        ("ok", FBool true)
    ]
    ignore my_data

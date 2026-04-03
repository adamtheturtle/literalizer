module Check

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        ("name", FStr "Alice");
        ("age", FInt 30L);
        ("active", FBool true);
        ("score", FNull)
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        ("name", FStr "Alice");
        ("age", FInt 30L);
        ("active", FBool true);
        ("score", FNull)
    ]
    ignore my_data

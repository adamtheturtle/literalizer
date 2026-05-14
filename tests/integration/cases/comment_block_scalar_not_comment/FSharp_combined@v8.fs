module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("description", FStr "# not a comment\n");
        ("name", FStr "foo")
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("description", FStr "# not a comment\n");
        ("name", FStr "foo")
    ]
    ignore my_data

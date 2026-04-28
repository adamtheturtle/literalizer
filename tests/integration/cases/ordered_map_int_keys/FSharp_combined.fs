module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("1", FStr "one");
        ("2", FStr "two");
        ("42", FStr "answer")
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("1", FStr "one");
        ("2", FStr "two");
        ("42", FStr "answer")
    ]
    ignore my_data

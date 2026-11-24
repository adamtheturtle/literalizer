module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("exact_millisecond", FStr (string (System.TimeOnly(9, 30, 15, 123))));
        ("sub_millisecond", FStr (string (System.TimeOnly(9, 30, 15, 123, 456))))
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("exact_millisecond", FStr (string (System.TimeOnly(9, 30, 15, 123))));
        ("sub_millisecond", FStr (string (System.TimeOnly(9, 30, 15, 123, 456))))
    ]
    ignore my_data

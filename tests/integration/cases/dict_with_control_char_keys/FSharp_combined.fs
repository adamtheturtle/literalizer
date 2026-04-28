module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("key\nwith\nnewlines", FStr "value1");
        ("key\twith\ttabs", FStr "value2");
        ("", FStr "value3")
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("key\nwith\nnewlines", FStr "value1");
        ("key\twith\ttabs", FStr "value2");
        ("", FStr "value3")
    ]
    ignore my_data

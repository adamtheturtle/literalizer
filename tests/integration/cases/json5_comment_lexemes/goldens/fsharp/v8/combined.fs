module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        // heading
        ("a", FStr "single ' // data");
        ("b", FStr "linecontinuation");
        ("c", FStr "\\");  // actual comment
        ("d", FStr "      ")  // final comment
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        // heading
        ("a", FStr "single ' // data");
        ("b", FStr "linecontinuation");
        ("c", FStr "\\");  // actual comment
        ("d", FStr "      ")  // final comment
    ]
    ignore my_data

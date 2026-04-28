module Main

type Val =
    | FStr of string
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FStr "line1\r\nline2";
        FStr "line1\rline2";
        FStr ""
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FStr "line1\r\nline2";
        FStr "line1\rline2";
        FStr ""
    ]
    ignore my_data

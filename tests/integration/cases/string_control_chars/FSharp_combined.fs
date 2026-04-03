module Check

type Val =
    | FStr of string
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FStr "line1\r\nline2";
        FStr "line1\rline2";
        FStr ""
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FStr "line1\r\nline2";
        FStr "line1\rline2";
        FStr ""
    ]
    ignore my_data

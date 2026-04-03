module Check

type Val =
    | FStr of string
    | FSet of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FSet [
        FStr "apple";
        FStr "banana";
        FStr "cherry"
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FSet [
        FStr "apple";
        FStr "banana";
        FStr "cherry"
    ]
    ignore my_data

module Check

type Val =
    | FFloat of float
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FFloat(-0.0);
        FFloat 1.5
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FFloat(-0.0);
        FFloat 1.5
    ]
    ignore my_data

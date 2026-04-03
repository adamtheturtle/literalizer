module Check

type Val =
    | FFloat of float
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FFloat infinity;
        FFloat(-infinity);
        FFloat nan
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FFloat infinity;
        FFloat(-infinity);
        FFloat nan
    ]
    ignore my_data

module Check

type Val =
    | FFloat of float
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FFloat 1.1;
        FFloat(-2.2);
        FFloat 3.3
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FFloat 1.1;
        FFloat(-2.2);
        FFloat 3.3
    ]
    ignore my_data

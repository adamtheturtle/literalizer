module Main

type Val =
    | FFloat of float
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FFloat 1.1;
        FFloat(-2.2);
        FFloat 3.3
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FFloat 1.1;
        FFloat(-2.2);
        FFloat 3.3
    ]
    ignore my_data

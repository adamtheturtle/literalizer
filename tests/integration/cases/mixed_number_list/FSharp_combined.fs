module Check

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FInt 1L;
        FFloat 2.5;
        FInt 3L
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FInt 1L;
        FFloat 2.5;
        FInt 3L
    ]
    ignore my_data

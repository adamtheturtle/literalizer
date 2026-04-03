module Check

type Val =
    | FFloat of float
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FList [FFloat 1.5; FFloat 2.5];
        FList [FFloat 3.5; FFloat 4.5]
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FList [FFloat 1.5; FFloat 2.5];
        FList [FFloat 3.5; FFloat 4.5]
    ]
    ignore my_data

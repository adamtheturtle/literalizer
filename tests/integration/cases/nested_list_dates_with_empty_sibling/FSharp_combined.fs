module Check

type Val =
    | FList of Val list
    | FStr of string
    | FDate of System.DateTime
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FList [FStr (string (System.DateOnly(2026, 1, 1))); FStr (string (System.DateOnly(2026, 1, 2)))];
        FList [];
        FList [FStr (string (System.DateOnly(2026, 2, 3))); FStr (string (System.DateOnly(2026, 2, 4)))]
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FList [FStr (string (System.DateOnly(2026, 1, 1))); FStr (string (System.DateOnly(2026, 1, 2)))];
        FList [];
        FList [FStr (string (System.DateOnly(2026, 2, 3))); FStr (string (System.DateOnly(2026, 2, 4)))]
    ]
    ignore my_data

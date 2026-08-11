module Main

type Val =
    | FList of Val list
    | FDatetime of System.DateTime
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FDatetime (System.DateTime(2024, 1, 15, 12, 30, 0));
        FDatetime (System.DateTime(2024, 6, 1, 8, 0, 0))
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FDatetime (System.DateTime(2024, 1, 15, 12, 30, 0));
        FDatetime (System.DateTime(2024, 6, 1, 8, 0, 0))
    ]
    ignore my_data

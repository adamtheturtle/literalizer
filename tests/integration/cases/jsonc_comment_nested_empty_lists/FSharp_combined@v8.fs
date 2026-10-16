module Main

type Val =
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        // outer heading
        // first empty
        FList [];
        // second empty
        FList []
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        // outer heading
        // first empty
        FList [];
        // second empty
        FList []
    ]
    ignore my_data

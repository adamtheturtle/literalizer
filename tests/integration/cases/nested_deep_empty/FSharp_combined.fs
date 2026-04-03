module Check

type Val =
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FList [FList []; FList []]
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FList [FList []; FList []]
    ]
    ignore my_data

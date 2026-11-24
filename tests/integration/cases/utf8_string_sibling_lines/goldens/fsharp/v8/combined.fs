module Main

type Val =
    | FStr of string
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FStr "中中中中中中中中中中中中中中中中中中中中";
        FStr "é'é'é'é'é'é'é'é'é'é'";
        FStr "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FStr "中中中中中中中中中中中中中中中中中中中中";
        FStr "é'é'é'é'é'é'é'é'é'é'";
        FStr "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
    ]
    ignore my_data

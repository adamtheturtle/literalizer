module Main

let private _mainDeclaration () =
    let mutable my_data = {|
        x = 1L
    |}
    ignore my_data

let private _mainAssignment () =
    let my_data = {|
        x = 1L
    |}
    ignore my_data

module Main

let private _mainDeclaration () =
    let mutable my_data = [
        {| active = true |};
        {| active = false |}
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data = [
        {| active = true |};
        {| active = false |}
    ]
    ignore my_data

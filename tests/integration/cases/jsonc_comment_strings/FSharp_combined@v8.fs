module Main

type Val =
    | FStr of string
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        // strings stay data
        FStr "https://example.org/a/*b*/";  // URL annotation
        FStr "escaped quote: \" // still data";
        FStr "backslash: \\";  // outside the string
        FStr "/* not a comment */"
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        // strings stay data
        FStr "https://example.org/a/*b*/";  // URL annotation
        FStr "escaped quote: \" // still data";
        FStr "backslash: \\";  // outside the string
        FStr "/* not a comment */"
    ]
    ignore my_data

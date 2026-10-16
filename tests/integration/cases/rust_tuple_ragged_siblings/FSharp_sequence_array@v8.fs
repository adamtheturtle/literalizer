module Main

type Val =
    | FStr of string
    | FList of Val array
let my_data: Val array = [|
    FList ([|FStr "set_task"; FStr "web"; FStr "lint_web"|]);
    FList ([|FStr "merge_pipelines"|])
|]

module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val array = [|
    [|FStr "set_task"; FStr "web"; FStr "lint_web"|];
    [|FStr "merge_pipelines"|]
|]

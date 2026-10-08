module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FList [FStr "set_task"; FStr "web"; FStr "lint_web"];
    FList [FStr "merge_pipelines"]
]

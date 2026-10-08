module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EStr "set_task", EStr "web", EStr "lint_web"],
    EList [EStr "merge_pipelines"]
    ]

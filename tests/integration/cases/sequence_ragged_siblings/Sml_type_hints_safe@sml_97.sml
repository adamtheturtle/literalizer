datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SList [SStr "set_task", SStr "web", SStr "lint_web"],
    SList [SStr "merge_pipelines"]
]
val _ = my_data

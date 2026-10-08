module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OList [OStr "set_task"; OStr "web"; OStr "lint_web"];
    OList [OStr "merge_pipelines"]
]

end

module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t array = [|
    [|OStr "set_task"; OStr "web"; OStr "lint_web"|];
    [|OStr "merge_pipelines"|]
|]

end

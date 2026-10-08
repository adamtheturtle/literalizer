module Check = struct

type val_t =
  | OStr of string
  | OArray of val_t array
let my_data : val_t array = [|
    OArray [|OStr "set_task"; OStr "web"; OStr "lint_web"|];
    OArray [|OStr "merge_pipelines"|]
|]

end

module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OStr "issue #{42}";
    OStr "color #red"
]

end

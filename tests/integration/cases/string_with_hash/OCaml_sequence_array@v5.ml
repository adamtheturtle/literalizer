module Check = struct

type val_t =
  | OStr of string
  | OArray of val_t array
let my_data : val_t array = [|
    OStr "issue #{42}";
    OStr "color #red"
|]

end

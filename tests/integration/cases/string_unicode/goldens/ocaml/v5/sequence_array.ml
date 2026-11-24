module Check = struct

type val_t =
  | OStr of string
  | OArray of val_t array
let my_data : val_t array = [|
    OStr "café";
    OStr "中文";
    OStr "😀"
|]

end

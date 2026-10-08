module Check = struct

type val_t =
  | OStr of string
  | OArray of val_t array
let my_data : val_t array = [|
    OStr "48656c6c6f"
|]

end

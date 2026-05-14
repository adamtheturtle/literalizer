module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t array = [|
    OStr "48656c6c6f"
|]

end

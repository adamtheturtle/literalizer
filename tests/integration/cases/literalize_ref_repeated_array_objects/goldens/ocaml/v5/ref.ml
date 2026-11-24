module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let shared : val_t array = [|
    OMap [("value", OInt 1)]
|]
let my_data : val_t array = [|
    OArray shared;
    OArray shared
|]

end

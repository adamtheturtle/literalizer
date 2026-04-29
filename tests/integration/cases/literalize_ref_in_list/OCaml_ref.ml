module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let x : val_t = OInt 0
let y : val_t = OInt 0
let my_data : val_t = OList [
    x;
    y
]

end

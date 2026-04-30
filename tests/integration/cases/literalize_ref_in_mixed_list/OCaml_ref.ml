module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let x : val_t = OMap [
    ("_", OStr "_")
]
let my_data : val_t = OList [
    x;
    OInt 1;
    OInt 2
]

end

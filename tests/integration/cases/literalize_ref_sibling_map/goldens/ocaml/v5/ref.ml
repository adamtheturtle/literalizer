module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let sibling_map : val_t = OMap [
    ("k", OInt 2)
]
let my_data : val_t = OList [
    OMap [("k", OInt 1)];
    sibling_map
]

end

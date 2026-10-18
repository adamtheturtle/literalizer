module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let string_map : val_t = OMap [
    ("k", OStr "s")
]
let my_data : val_t = OList [
    string_map;
    OMap [("k", OInt 1)]
]

end

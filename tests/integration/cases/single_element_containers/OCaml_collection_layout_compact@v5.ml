module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("single_map", OList [OMap []]);
    ("single_list", OList [OList [OInt 1]]);
    ("single_deep", OList [OList [OList [OInt 2]]])
]

end

module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("d", OList [OMap [("a", OList [OMap [("b", OList [OInt 1; OList [OFloat 2.5; OList [OStr "x"; OList [OBool true]]]])]])]])
]

end

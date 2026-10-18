module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("h", OList [OInt 1; OStr "a"; OList [OInt 2; OStr "b"]; OMap [("k", OList [OBool true])]])
]

end

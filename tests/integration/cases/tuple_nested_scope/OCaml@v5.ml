module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("x", OList [OInt 1; OList [OInt 2; OList [OInt 3]]])
]

end

module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OList [OMap [("a", OInt 1)]];
    OList [OMap [("a", OInt 2)]]
]

end

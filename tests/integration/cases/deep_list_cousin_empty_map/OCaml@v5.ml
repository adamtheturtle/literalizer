module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("items", OList [OMap [("inner", OMap [("x", OInt 1)])]; OMap [("inner", OMap [])]])];
    OMap [("items", OList [OMap [("inner", OMap [("x", OInt 2)])]; OMap [("inner", OMap [])]])]
]

end

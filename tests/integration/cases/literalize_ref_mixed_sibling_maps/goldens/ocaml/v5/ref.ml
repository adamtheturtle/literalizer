module Check = struct

type val_t =
  | ONull
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let actual : val_t = OInt 42
let my_data : val_t = OList [
    OMap [("$ref", OInt 1)];
    OMap [("$ref", ONull)];
    actual
]

end

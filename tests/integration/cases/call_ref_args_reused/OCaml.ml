module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OList [OMap [("$ref", OStr "repeated_var")]; OInt 1];
    OList [OMap [("$ref", OStr "single_var")]; OInt 0];
    OList [OMap [("$ref", OStr "repeated_var")]; OInt 8]
]

end

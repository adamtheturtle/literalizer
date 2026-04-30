module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OList [OList [OMap [("$ref", OStr "my_var")]; OInt 42; OStr "static"]];
    OList [OList [OMap [("$ref", OStr "my_other")]; OInt 7; OStr "label"]]
]

end

module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OList [OList [OMap [("$ref", OStr "myVar")]; OInt 42; OStr "static"]]
]

end

module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", OMap [("b", OMap [("c", OMap [("$ref", OStr "deep")])])])
]

end

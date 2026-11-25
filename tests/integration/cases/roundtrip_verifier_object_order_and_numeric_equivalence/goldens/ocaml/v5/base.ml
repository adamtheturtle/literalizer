module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("b", ONull);
    ("a", OMap [("y", OList [OFloat 1.0]); ("x", OBool false)])
]

end

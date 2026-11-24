module Check = struct

type val_t =
  | ONull
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    (* comment *)
    ("name", OStr "Alice");
    ("score", ONull)
]

end

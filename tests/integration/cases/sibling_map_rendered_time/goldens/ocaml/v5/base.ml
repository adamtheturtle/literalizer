module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", OMap [("k", OStr "07:30:00")]);
    ("b", OMap [("k", OStr "string")])
]

end

module Check = struct

type val_t =
  | OFloat of float
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("value", OFloat 0.0)
]

end

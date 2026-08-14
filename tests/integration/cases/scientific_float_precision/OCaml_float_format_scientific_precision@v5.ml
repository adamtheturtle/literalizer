module Check = struct

type val_t =
  | OFloat of float
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("value", OFloat 1.2345678901234567)
]

end

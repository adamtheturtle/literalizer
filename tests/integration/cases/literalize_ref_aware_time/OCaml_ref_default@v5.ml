module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let value : val_t = OStr "12:30:15+02:00"
let my_data : val_t = OMap [
    ("x", value)
]

end

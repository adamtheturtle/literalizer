module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let shared : val_t = OStr "s"
let my_data : val_t = OMap [
    ("value", shared)
]

end

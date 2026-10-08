module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let existing : val_t = OMap [
    ("_", OStr "_")
]
let my_data : val_t = existing

end

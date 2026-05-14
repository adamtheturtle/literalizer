module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("morning", OStr "09:30:00");
    ("afternoon", OStr "14:15:00");
    ("evening", OStr "23:59:59")
]

end

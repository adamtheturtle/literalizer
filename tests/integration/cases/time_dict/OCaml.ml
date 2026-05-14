module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("morning", "09:30:00");
    ("afternoon", "14:15:00");
    ("evening", "23:59:59")
]

end

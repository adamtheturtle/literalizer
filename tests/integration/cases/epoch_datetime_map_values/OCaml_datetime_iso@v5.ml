module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("within_i32", OStr "2024-01-15T12:00:00");
    ("beyond_i32", OStr "2099-06-15T08:30:00")
]

end

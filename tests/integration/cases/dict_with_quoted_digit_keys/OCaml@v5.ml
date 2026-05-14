module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("0a", OStr "first");
    ("1b", OStr "second")
]

end

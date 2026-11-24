module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("x", OStr "\000");
    ("y", OStr "\0001")
]

end

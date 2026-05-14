module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let val_x : val_t = OMap [
    ("_", OStr "_")
]
let val_y : val_t = OMap [
    ("_", OStr "_")
]
let my_data : val_t = OList [
    val_x;
    val_y
]

end

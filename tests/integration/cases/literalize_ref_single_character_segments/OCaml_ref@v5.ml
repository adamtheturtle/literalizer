module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let a_b_c : val_t = OMap [
    ("_", OStr "_")
]
let my_data : val_t = a_b_c

end

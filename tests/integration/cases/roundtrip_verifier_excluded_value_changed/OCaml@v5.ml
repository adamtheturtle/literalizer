module Check = struct

type val_t =
  | OBool of bool
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("keep", OBool true);
    ("skip", OBool false)
]

end

module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("host", OStr "localhost");
    ("port", ONull);  (* not configured yet *)
    ("debug", OBool true)
]

end

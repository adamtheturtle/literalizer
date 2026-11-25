module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    (* outer heading *)
    (* first empty *)
    ("a", OMap []);
    (* second empty *)
    ("b", OMap [])
]

end

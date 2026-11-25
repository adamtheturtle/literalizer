module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("host", OStr "it's here");  (* a comment *)
    ("port", OInt 80)  (* another *)
]

end

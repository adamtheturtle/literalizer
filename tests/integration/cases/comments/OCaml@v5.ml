module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    (* Server configuration *)
    ("host", OStr "localhost");  (* default host *)
    ("port", OInt 8080);
    (* Enable debug mode *)
    ("debug", OBool true)
]

end

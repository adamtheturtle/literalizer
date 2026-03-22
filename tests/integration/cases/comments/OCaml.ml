module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
  | OSet of val_t list

let x : val_t = OMap [
    (* Server configuration *)
    ("host", OStr "localhost");  (* default host *)
    ("port", OInt 8080);
    (* Enable debug mode *)
    ("debug", OBool true)
]

end

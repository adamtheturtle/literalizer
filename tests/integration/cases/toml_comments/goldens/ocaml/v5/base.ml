module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    (* before *)
    ("answer", OInt 42);  (* inline *)
    ("plain", OStr "ok")
    (* trailing *)
]

end

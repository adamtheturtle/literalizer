module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let send _ = ()
let _ = send(OMap [("a", OInt 1); ("b", OStr "x")])

end

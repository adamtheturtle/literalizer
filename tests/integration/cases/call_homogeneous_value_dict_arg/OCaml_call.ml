module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let process _ = ()
let _ = process(OMap [("a", OInt 1); ("b", OInt 2)])

end

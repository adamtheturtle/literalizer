module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let process _ = ()
let my_var : val_t = OInt 42
let _ = process(OMap [("key", OMap [("ref", OStr "my_var")]); ("count", OInt 42)])

end

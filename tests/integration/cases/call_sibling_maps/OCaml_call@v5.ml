module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let process _ = ()
let _ = process(OMap [("value", OInt 1)])
let _ = process(OMap [("value", OStr "hello")])

end

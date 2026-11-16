module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let consume _ = ()
let item : val_t = OInt 42
let _ = consume(OMap [("field", item)])

end

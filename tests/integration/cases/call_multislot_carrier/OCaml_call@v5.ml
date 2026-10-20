module Check = struct

let process _ = ()
type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
let _ = process(OInt 1, OStr "hello")
let _ = process(OStr "two", OBool false)
let _ = process(OFloat 3.5, ONull)

end

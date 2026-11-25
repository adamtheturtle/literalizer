module Check = struct

let process _ = ()
type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
let _ = process(OStr "hello")
let _ = process(OInt 42)
let _ = process(OBool true)
let _ = process(ONull)

end

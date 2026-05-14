module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
let process _ = ()
let _ = process("hello")
let _ = process(42)
let _ = process(OBool true)

end

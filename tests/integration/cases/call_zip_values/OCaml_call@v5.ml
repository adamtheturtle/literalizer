module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
let process _ = ()
let emit _ = ()
let _ = emit(process(OStr "hello"), OBool true)
let _ = emit(process(OInt 42), OBool false)

end

module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OList of val_t list
let process _ = ()
let emit _ = ()
let _ = emit(process(42), OBool true)

end

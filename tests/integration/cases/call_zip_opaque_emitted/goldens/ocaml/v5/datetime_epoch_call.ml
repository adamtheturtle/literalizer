module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let emit _ = ()
let _ = emit(process(OInt 1), OInt 1705320000)

end

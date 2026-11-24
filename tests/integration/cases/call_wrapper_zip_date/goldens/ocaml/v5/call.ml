module Check = struct

type val_t =
  | OInt of int
  | ODate of (int * int * int)
  | OList of val_t list
let process _ = ()
let emit _ = ()
let _ = emit(process(OInt 1), ODate (2024, 1, 15))

end

module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OList of val_t list
let process _ = ()
let emit _ = ()
let _ = emit(process(OInt 1), OFloat 1.5)

end

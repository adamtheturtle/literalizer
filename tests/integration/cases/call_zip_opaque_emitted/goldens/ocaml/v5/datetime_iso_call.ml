module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let process _ = ()
let emit _ = ()
let _ = emit(process(OInt 1), OStr "2024-01-15T12:00:00")

end

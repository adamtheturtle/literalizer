module Check = struct

type val_t =
  | OInt of int
  | ODatetime of ((int * int * int) * (int * int * int))
  | OList of val_t list
let process _ = ()
let emit _ = ()
let _ = emit(process(OInt 1), ODatetime ((2024, 1, 15), (12, 0, 0)))

end

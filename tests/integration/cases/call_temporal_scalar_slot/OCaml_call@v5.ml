module Check = struct

type val_t =
  | OInt of int
  | ODatetime of ((int * int * int) * (int * int * int))
  | OList of val_t list
let process _ = ()
let _ = process("09:30:00")
let _ = process(ODatetime ((2024, 1, 15), (0, 0, 0)))
let _ = process(1)

end

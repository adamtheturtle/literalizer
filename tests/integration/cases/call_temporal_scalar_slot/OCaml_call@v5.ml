module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | ODatetime of ((int * int * int) * (int * int * int))
  | OList of val_t list
let process _ = ()
let _ = process(OStr "09:30:00")
let _ = process(ODatetime ((2024, 1, 15), (0, 0, 0)))
let _ = process(OInt 1)

end

module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let _ = process(1, 2, 3, 4)
let _ = process(5, 6, 7, 8)

end

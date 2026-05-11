module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let _ = process(1, 2, 3, 4)
let _ = process(10, 20, 30, 40)

end

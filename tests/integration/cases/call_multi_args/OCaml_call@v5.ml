module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let _ = process(1, 42)
let _ = process(2, 100)

end

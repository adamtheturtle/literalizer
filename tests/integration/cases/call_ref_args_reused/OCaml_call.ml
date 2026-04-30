module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let shared : val_t = OInt 1
let other : val_t = OInt 2
let _ = process(shared, 1)
let _ = process(other, 0)
let _ = process(shared, 8)

end

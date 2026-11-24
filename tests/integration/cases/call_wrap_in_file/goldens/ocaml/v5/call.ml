module Check = struct

let process _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = process(OInt 1, OInt 2)
let _ = process(OInt 3, OInt 4)

end

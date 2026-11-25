module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let _ = process(OInt 1, OInt 2, OInt 3, OInt 4)
let _ = process(OInt 5, OInt 6, OInt 7, OInt 8)

end

module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let _ = process(OInt 1, OInt 42)
let _ = process(OInt 2, OInt 100)

end

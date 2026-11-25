module Check = struct

type val_t =
  | ONull
  | OInt of int
  | OList of val_t list
let process _ = ()
let _ = process(ONull)
let _ = process(OList [OInt 1; OInt 2])

end

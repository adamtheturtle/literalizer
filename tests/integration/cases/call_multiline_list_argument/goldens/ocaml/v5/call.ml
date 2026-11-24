module Check = struct

let process _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = process(OList [
    OInt 1;
    OInt 2
])
let _ = process(OList [
    OInt 3
])

end

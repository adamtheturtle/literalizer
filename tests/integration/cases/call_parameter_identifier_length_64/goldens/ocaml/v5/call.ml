module Check = struct

let f _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = f(OInt 1)

end

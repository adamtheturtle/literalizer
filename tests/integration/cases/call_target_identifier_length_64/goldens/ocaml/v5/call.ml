module Check = struct

let ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff(OInt 1)

end

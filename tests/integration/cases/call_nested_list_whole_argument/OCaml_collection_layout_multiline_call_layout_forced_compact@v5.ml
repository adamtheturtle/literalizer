module Check = struct

let f _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = f(OList [OList [OInt 1; OInt 2]; OList [OInt 3]])

end

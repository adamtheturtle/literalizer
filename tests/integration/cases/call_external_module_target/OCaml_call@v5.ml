module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let _ = Stdlib.ignore(OInt 1)

end

module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let consume _ = ()
let _ = consume(OInt 1)

end

module Check = struct

let consume _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = consume(OInt (-2147483649))
let _ = consume(OInt 2147483648)

end

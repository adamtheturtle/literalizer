module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let consume _ = ()
let external_value : val_t = OInt 1
let _ = consume(external_value)

end

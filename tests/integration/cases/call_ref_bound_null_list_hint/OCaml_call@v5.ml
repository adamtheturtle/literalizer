module Check = struct

type val_t =
  | ONull
  | OInt of int
  | OList of val_t list
let consume _ = ()
let item : val_t = ONull
let _ = consume(item)

end

module Check = struct

let do_thing _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = do_thing(OInt 1)
let _ = do_thing(OInt 2)

end

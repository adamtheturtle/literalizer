module Check = struct

let process _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = process(1, 2)

end

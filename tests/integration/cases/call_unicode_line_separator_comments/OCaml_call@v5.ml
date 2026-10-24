module Check = struct

let process _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = process(OInt 1)  (* note<U+2028>still commented<U+2029>done *)

end

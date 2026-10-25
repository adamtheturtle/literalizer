module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let f _ = ()
let _ = f(OList [OInt 1])  (* note *)

end

module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let _ = process(OInt 1)  (* trail \ *)
let _ = process(OInt 2)  (* second *)

end

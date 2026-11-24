module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let f _ = ()
(* selected heading *)
let _ = f(OInt 1, OInt 2)  (* selected inline *)

end

module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let f _ = ()
(* calls heading *)
(* before call one *)
(* first argument *)
let _ = f(OInt 1, OInt 2)  (* after call one *)
(* second argument *)
let _ = f(OInt 3, OInt 4)
(* after all calls *)

end

module Check = struct

type val_t =
  | OInt of int
let f _ = ()
(* scalar heading *)
(* second heading line *)
(* scalar inline *)
(* inline continuation *)
(* scalar trailing *)
let _ = f(OInt 42)

end

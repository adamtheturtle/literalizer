module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let f _ = ()
let _ = f(OInt 2, OStr "hello")  (* trailing note *)
let _ = f(OInt 3, OStr "world")  (* another note *)

end

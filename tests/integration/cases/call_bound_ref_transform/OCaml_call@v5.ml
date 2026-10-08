module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let f _ = ()
let x : val_t = OInt 1
let _ = f(x)

end

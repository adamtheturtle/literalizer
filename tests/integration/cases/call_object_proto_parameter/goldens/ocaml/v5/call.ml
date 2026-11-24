module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let capture _ = ()
let _ = capture(OInt 1)

end

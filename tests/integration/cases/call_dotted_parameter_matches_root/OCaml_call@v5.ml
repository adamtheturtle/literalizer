module Check = struct

module Outer = struct
let inner _ = ()
end
type val_t =
  | OInt of int
  | OList of val_t list
let _ = Outer.inner(OInt 1, OInt 2)

end

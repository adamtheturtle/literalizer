module Check = struct

let check _ = ()
type val_t =
  | OInt of int
let _ = check(OInt 42)

end

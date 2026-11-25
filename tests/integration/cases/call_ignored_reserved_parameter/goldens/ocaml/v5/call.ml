module Check = struct

let process _ = ()
type val_t =
  | OInt of int
let _ = process(OInt 42)

end

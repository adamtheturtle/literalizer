module Check = struct

type val_t =
  | OInt of int
let process _ = ()
let value : val_t = OInt 1
let _ = process(value)

end

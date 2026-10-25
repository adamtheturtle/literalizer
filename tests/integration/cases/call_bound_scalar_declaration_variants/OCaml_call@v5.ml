module Check = struct

type val_t =
  | OInt of int
let consume _ = ()
let shared : val_t = OInt 42
let _ = consume(shared)

end

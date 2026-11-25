module Check = struct

let check_wrapper _ = ()
type val_t =
  | OInt of int
let _ = check_wrapper(OInt 42)

end

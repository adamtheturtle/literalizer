module Check = struct

type val_t =
  | OInt of int
let process _ = ()
let emit _ = ()
let _ = emit(process(OInt 42))

end

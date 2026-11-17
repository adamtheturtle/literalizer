module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
module Module = struct
  let func _ = ()
end
let _ = Module.func(OInt 1)

end

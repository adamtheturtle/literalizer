module Check = struct

module Module = struct
  let func _ = ()
end
type val_t =
  | OInt of int
  | OList of val_t list
let _ = Module.func(OInt 1)

end

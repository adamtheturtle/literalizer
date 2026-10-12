module Check = struct

type val_t =
  | OInt of int
module Obj = struct
let ZKV _ = ()
end
let _ = Obj.ZKV(OInt 1)

end

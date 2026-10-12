module Check = struct

type val_t =
  | OInt of int
module Obj = struct
let ZVal _ = ()
end
let _ = Obj.ZVal(OInt 1)

end

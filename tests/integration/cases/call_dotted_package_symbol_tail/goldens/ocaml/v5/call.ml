module Check = struct

module Helper = struct
let list _ = ()
end
type val_t =
  | OInt of int
  | OList of val_t list
let _ = Helper.list(OInt 1)

end

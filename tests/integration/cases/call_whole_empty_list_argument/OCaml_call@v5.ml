module Check = struct

let f _ = ()
type val_t =
  | OList of val_t list
let _ = f(OList [])

end

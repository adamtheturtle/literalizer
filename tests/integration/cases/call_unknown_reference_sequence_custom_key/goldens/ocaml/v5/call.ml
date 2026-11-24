module Check = struct

type val_t =
  | OList of val_t list
let process _ = ()
let untyped_value : val_t = OList []
let _ = process(OList [untyped_value; untyped_value])

end

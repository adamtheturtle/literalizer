module Check = struct

type val_t =
  | OList of val_t list
let process _ = ()
let unknown_value : val_t = OList []
let _ = process(OList [unknown_value])

end

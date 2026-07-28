module Check = struct

type val_t =
  | OBool of bool
  | OList of val_t list
let process _ = ()
let known_value : val_t = OBool true
let unknown_value : val_t = OBool true
let _ = process(known_value, OList [unknown_value])

end

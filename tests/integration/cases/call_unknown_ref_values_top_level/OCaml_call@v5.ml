module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let known_value : val_t = OInt 1
let unknown_value : val_t = OList []
let _ = process(unknown_value)

end

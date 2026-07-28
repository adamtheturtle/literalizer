module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let unknown_value : val_t = OList [
    OInt 1
]
let _ = process(unknown_value)

end

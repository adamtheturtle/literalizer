module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let item : val_t = OList [
    OInt 1;
    OInt 2
]
let _ = process(item)

end

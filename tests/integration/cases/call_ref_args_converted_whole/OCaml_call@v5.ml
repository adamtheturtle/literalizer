module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let my_var : val_t = OList [
    OInt 1;
    OInt 2;
    OInt 3
]
let _ = process(my_var)

end

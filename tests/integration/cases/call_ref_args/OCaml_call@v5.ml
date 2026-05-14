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
let my_other : val_t = OList [
    OInt 4;
    OInt 5;
    OInt 6
]
let _ = process(my_var, 42)
let _ = process(my_other, 7)

end

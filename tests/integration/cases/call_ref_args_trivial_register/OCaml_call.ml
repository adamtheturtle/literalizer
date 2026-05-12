module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OList of val_t list
let process _ = ()
let my_int : val_t = OInt 1
let my_bool : val_t = OBool true
let my_float : val_t = OFloat 3.14
let my_list : val_t = OList [
    OInt 1;
    OInt 2;
    OInt 3
]
let _ = process(my_int, 42)
let _ = process(my_bool, 7)
let _ = process(my_float, 9)
let _ = process(my_list, 1)

end

module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let repeated_var : val_t = OInt 1
let single_var : val_t = OList [
    OInt 4;
    OInt 5;
    OInt 6
]
let _ = process(repeated_var, 1)
let _ = process(single_var, 0)
let _ = process(repeated_var, 8)

end

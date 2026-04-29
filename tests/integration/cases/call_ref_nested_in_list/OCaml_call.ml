module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let process _ = ()
let my_var : val_t = OInt 42
let my_other : val_t = OInt 7
let _ = process(OList [my_var; OInt 42; OStr "static"])
let _ = process(OList [my_other; OInt 7; OStr "label"])

end

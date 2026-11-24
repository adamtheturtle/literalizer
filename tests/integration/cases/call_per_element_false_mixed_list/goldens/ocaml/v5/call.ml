module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let process _ = ()
let _ = process(OList [OInt 1; OStr "x"])

end

module Check = struct

let make_widget _ = ()
type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let _ = make_widget(OList [OInt 1], OList [OStr "text"])

end

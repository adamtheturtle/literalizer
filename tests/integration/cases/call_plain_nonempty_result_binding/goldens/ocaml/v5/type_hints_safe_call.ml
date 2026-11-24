module Check = struct

let make_widget _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let my_data = make_widget(OList [OInt 1])

end

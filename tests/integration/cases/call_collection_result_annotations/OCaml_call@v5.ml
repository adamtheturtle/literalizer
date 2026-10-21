module Check = struct

let make_widget _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let my_data = make_widget(OList [OList [OInt 1; OInt 2]; OList [OInt 3]])

end

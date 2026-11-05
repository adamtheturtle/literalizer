module Check = struct

let make_widget _ = ()
type val_t =
  | OList of val_t list
let _ = make_widget(OList [])

end

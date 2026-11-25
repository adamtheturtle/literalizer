module Check = struct

type val_t =
  | OList of val_t list
let make_widget _ = ()
let items : val_t = OList []
let _ = make_widget(items)

end

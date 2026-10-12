module Check = struct

type val_t =
  | OInt of int
let make_widget _ = ()
let my_data : val_t = OInt 42
let my_data = make_widget(my_data) // note
let _ = make_widget(my_data)

end

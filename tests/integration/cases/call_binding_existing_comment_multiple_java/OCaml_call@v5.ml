module Check = struct

type val_t =
  | ONull
  | OInt of int
let make_widget _ = ()
let my_data : val_t = ONull
let my_data = make_widget(OInt 42) // note
// extra

end

module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let consume_widget _ = ()
let shared : val_t = OInt 1
let my_data : val_t = shared
let _ = consume_widget(my_data)

end

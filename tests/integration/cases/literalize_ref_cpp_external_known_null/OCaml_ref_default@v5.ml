module Check = struct

type val_t =
  | ONull
  | OList of val_t list
let consume_widget _ = ()
let item : val_t = ONull
let my_data : val_t = ONull
let _ = consume_widget(my_data)
let my_data : val_t = item
let _ = consume_widget(my_data)

end

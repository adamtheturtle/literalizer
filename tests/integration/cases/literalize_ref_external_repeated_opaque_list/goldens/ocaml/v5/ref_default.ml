module Check = struct

type val_t =
  | OList of val_t list
let consume_widget _ = ()
let item : val_t = OList []
let my_data : val_t = OList [
    item;
    item
]
let _ = consume_widget(my_data)

end

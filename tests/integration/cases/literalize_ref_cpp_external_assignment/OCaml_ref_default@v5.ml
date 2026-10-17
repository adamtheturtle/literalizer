module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let consume_widget _ = ()
let ref_data : val_t = OList [
    OInt 1;
    OInt 2
]
let my_data : val_t = OList [
    OInt 0
]
let _ = consume_widget(my_data)
let my_data : val_t = ref_data
let _ = consume_widget(my_data)

end

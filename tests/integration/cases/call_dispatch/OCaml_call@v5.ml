module Check = struct

let store_item _ = ()
let read_item _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = store_item(1, 10)
let _ = read_item(1)

end

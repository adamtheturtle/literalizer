module Check = struct

let record_entry _ = ()
type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
let my_data = record_entry(OStr "a", OInt 1, OBool true)

end

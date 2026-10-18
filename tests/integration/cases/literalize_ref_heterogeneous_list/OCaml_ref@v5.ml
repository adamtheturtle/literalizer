module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let one : val_t = OInt 1
let two : val_t = OStr "s"
let my_data : val_t = OList [
    one;
    two
]

end

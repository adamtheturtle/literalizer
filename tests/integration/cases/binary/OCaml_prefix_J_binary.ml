module Check = struct

type val_t =
  | JStr of string
  | JList of val_t list
let my_data : val_t = JList [
    JStr "48656c6c6f"
]

end

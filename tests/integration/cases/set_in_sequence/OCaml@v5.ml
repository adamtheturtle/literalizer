module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OSet of val_t list
let my_data : val_t = OList [
    OSet [OStr "a"; OStr "b"]
]

end

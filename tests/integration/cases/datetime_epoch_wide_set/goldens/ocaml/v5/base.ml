module Check = struct

type val_t =
  | ODatetime of ((int * int * int) * (int * int * int))
  | OSet of val_t list
let my_data : val_t = OSet [
    ODatetime ((2099, 6, 15), (8, 30, 0))
]

end

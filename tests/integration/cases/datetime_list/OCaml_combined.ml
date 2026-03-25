module Check = struct

type val_t =
  | ODatetime of ((int * int * int) * (int * int * int))
  | OList of val_t list
let my_data : val_t = OList [
    ODatetime ((2024, 1, 15), (12, 30, 0));
    ODatetime ((2024, 6, 1), (8, 0, 0))
]

end

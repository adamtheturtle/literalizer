module Check = struct

type val_t =
  | ODatetime of ((int * int * int) * (int * int * int))
  | OSet of val_t list
let my_data : val_t = OSet [
    ODatetime ((1901, 12, 13), (20, 45, 51));
    ODatetime ((1901, 12, 13), (20, 45, 52));
    ODatetime ((2038, 1, 19), (3, 14, 7));
    ODatetime ((2038, 1, 19), (3, 14, 8))
]

end

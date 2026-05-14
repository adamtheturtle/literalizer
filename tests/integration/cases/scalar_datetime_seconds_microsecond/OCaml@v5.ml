module Check = struct

type val_t =
  | ODatetime of ((int * int * int) * (int * int * int))
let my_data : val_t = ODatetime ((2024, 1, 15), (12, 30, 45))

end

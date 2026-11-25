module Check = struct

type val_t =
  | ODatetime of ((int * int * int) * (int * int * int))
let my_data : val_t = ODatetime ((1901, 12, 13), (20, 45, 51))

end

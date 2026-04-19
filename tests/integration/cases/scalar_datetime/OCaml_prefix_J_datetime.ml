module Check = struct

type val_t =
  | JDatetime of ((int * int * int) * (int * int * int))
let my_data : val_t = JDatetime ((2024, 1, 15), (12, 30, 0))

end

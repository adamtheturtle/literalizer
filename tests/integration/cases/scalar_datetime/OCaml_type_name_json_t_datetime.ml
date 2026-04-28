module Check = struct

type json_t =
  | ODatetime of ((int * int * int) * (int * int * int))
let my_data : json_t = ODatetime ((2024, 1, 15), (12, 30, 0))

end

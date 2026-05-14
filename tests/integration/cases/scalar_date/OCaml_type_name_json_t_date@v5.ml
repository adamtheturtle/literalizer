module Check = struct

type json_t =
  | ODate of (int * int * int)
let my_data : json_t = ODate (2024, 1, 15)

end

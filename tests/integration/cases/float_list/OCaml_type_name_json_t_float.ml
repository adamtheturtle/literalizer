module Check = struct

type json_t =
  | OFloat of float
  | OList of json_t list
let my_data : json_t = OList [
    OFloat 1.1;
    OFloat (-2.2);
    OFloat 3.3
]

end

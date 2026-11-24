module Check = struct

type json_t =
  | OFloat of float
  | OList of json_t list
let my_data : json_t = OList [
    OFloat infinity;
    OFloat neg_infinity;
    OFloat nan
]

end

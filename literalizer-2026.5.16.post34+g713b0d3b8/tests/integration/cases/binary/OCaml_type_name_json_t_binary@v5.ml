module Check = struct

type json_t =
  | OStr of string
  | OList of json_t list
let my_data : json_t = OList [
    OStr "48656c6c6f"
]

end

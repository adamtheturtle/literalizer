module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("level1", OMap [("level2", OMap [("level3", OMap [("level4", OMap [("value", OStr "deep"); ("items", OList [OStr "a"; OStr "b"])])]); ("sibling", OInt 42)]); ("tags", OList [OMap [("name", OStr "tag1"); ("meta", OMap [("priority", OInt 1); ("labels", OList [OStr "x"; OStr "y"])])]])])
]

end

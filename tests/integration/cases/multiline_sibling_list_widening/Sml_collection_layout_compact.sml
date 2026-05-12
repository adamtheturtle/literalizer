datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("sibling_lists", SMap [("numbers", SList [SInt 1, SInt 2]), ("strings", SList [SStr "x", SStr "y"])]),
    ("ref_marker_present", SList [SStr "$keep", SStr "z"])
]
val _ = my_data

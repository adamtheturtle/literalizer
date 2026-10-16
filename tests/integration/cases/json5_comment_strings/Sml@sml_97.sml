datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    (* strings stay data *)
    SStr "https://example.org/a/*b*/",  (* URL annotation *)
    SStr "escaped quote: \" // still data",
    SStr "backslash: \\",  (* outside the string *)
    SStr "/* not a comment */"
]
val _ = my_data

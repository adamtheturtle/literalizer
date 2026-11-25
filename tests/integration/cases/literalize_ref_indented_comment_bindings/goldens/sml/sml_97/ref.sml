datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
        val shared : val_t = SList [
            SInt 1,
            SInt 2
        ]
        val my_data : val_t = SList [
            (* A leading comment with { braces, quotes, and // markers *)
            SStr "first\n{ \"quoted\" // text }",
            shared
        ]
val _ = my_data

module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
        let shared : val_t = OList [
            OInt 1;
            OInt 2
        ]
        let my_data : val_t = OList [
            (* A leading comment with { braces, quotes, and // markers *)
            OStr "first\n{ \"quoted\" // text }";
            shared
        ]

end

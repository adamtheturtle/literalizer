module Main

        type Val =
            | FInt of int64
            | FStr of string
            | FList of Val list
        let shared: Val = FList [
            FInt 1L;
            FInt 2L
        ]
        let my_data: Val = FList [
            // A leading comment with { braces, "quotes", and // markers
            FStr "first\n{ \"quoted\" // text }";
            shared
        ]

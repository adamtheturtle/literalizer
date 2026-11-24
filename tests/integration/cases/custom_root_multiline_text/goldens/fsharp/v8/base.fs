module Main

type Val =
    | FStr of string
let custom_data: Val = FStr "head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail"

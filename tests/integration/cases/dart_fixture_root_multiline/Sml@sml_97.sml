datatype val_t =
    SStr of string
val custom_data : val_t = SStr "head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail"
val _ = custom_data

module Check = struct

type val_t =
  | OStr of string
let custom_data : val_t = OStr "head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail"

end

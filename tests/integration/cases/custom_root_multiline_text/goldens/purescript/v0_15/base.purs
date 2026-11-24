module Check where


data Val
    = PStr String


custom_data :: Val
custom_data = PStr "head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail"

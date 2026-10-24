module Check exposing (..)


type Val
    = EStr String


custom_data : Val
custom_data = EStr "head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail"

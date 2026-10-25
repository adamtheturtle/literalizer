-module(fixture_custom_root_multiline_text_erlang).
-export([x/0]).
x() ->
    Custom_data = "head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail",
    Custom_data.

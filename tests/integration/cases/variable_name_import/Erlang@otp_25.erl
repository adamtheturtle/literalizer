-module(fixture_variable_name_import_erlang).
-export([x/0]).
x() ->
    Import = 1,
    Import.

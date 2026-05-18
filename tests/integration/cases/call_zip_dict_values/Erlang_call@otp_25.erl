-module(fixture_call_zip_dict_values_erlang_call).
-export([x/0]).
process(_) -> undefined.
emit(_, _) -> ok.
x() ->
    emit(process("hello"), #{"a" => 1, "b" => 2}),
    emit(process(42), #{"c" => 3, "d" => 4}).

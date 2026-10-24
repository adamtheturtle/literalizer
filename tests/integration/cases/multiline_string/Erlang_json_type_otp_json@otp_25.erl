-module(fixture_multiline_string_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"first line\n  indented\n\nlast line"/utf8>>,
        <<"\nleading newline"/utf8>>,
        <<" \t\nleading whitespace"/utf8>>,
        <<"trailing newline\n"/utf8>>,
        <<"\nleading and trailing\n"/utf8>>,
        <<"quotes: \"\"\" ''' ` and backslash: \\"/utf8>>,
        <<"interpolation: ${value} #{value} #@value #$value $value"/utf8>>,
        <<"backslash before newline: \\\nnext line"/utf8>>,
        <<"trailing spaces  \nnext"/utf8>>,
        <<"C++ empty delimiter collision: )\"\nvalue"/utf8>>,
        <<"C++ first fallback collision: )\" and )x\"\nvalue"/utf8>>,
        <<"C++ second fallback collision: )\" and )x\" and )x0\"\nvalue"/utf8>>,
        <<"Rust delimiter collision: \"#\nvalue"/utf8>>,
        <<"Lua delimiter collision: ]]\nvalue"/utf8>>,
        <<"Swift delimiter collision: \"\"\"#\nvalue"/utf8>>,
        <<"Swift interpolation collision: \\#(value)\nvalue"/utf8>>,
        <<"Ruby fallback interpolation  \n#{expression} #@instance #$global"/utf8>>,
        <<"NUL followed by a digit: \x{0}7"/utf8>>,
        <<"carriage\rreturn"/utf8>>
    ],
    My_data.

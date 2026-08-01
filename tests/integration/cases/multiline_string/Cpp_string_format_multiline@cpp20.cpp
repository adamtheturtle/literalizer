#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    R"LITERALIZER(first line
  indented

last line)LITERALIZER",
    R"LITERALIZER(
leading newline)LITERALIZER",
    " \t\nleading whitespace",
    R"LITERALIZER(trailing newline
)LITERALIZER",
    R"LITERALIZER(
leading and trailing
)LITERALIZER",
    R"LITERALIZER(quotes: """ ''' ` and backslash: \)LITERALIZER",
    R"LITERALIZER(interpolation: ${value} #{value} #@value #$value $value)LITERALIZER",
    R"LITERALIZER(backslash before newline: \
next line)LITERALIZER",
    "trailing spaces  \nnext",
    R"LITERALIZER0(C++ delimiter collision: )LITERALIZER"
value)LITERALIZER0",
    R"LITERALIZER(Rust delimiter collision: "#
value)LITERALIZER",
    R"LITERALIZER(Lua delimiter collision: ]]
value)LITERALIZER",
    "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    std::string{"NUL followed by a digit: "} + '\0' + "7",
    "carriage\rreturn",
};
    (void)my_data;
    return 0;
}

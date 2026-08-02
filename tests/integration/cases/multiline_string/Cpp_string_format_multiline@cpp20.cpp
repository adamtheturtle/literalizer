#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    R"(first line
  indented

last line)",
    R"(
leading newline)",
    " \t\nleading whitespace",
    R"(trailing newline
)",
    R"(
leading and trailing
)",
    R"(quotes: """ ''' ` and backslash: \)",
    R"(interpolation: ${value} #{value} #@value #$value $value)",
    R"(backslash before newline: \
next line)",
    "trailing spaces  \nnext",
    R"x(C++ empty delimiter collision: )"
value)x",
    R"x0(C++ first fallback collision: )" and )x"
value)x0",
    R"x1(C++ second fallback collision: )" and )x" and )x0"
value)x1",
    R"(Rust delimiter collision: "#
value)",
    R"(Lua delimiter collision: ]]
value)",
    R"(Swift delimiter collision: """#
value)",
    R"(Swift interpolation collision: \#(value)
value)",
    "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    std::string{"NUL followed by a digit: "} + '\0' + "7",
    "carriage\rreturn",
};
    (void)my_data;
    return 0;
}

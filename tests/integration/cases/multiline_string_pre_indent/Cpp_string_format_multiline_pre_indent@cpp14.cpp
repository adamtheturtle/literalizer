#include <string>

int main() {
    const auto* my_data = R"(
first line
  indented

last line
)";
    return std::string(my_data) == "\nfirst line\n  indented\n\nlast line\n" ? 0 : 1;
}

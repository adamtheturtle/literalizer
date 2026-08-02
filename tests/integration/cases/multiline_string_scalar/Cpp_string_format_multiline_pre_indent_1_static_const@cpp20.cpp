#include <initializer_list>
#include <string>
int main() {
    static const auto* my_data = R"(first line
  indented

last line)";
    (void)my_data;
    return 0;
}

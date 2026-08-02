#include <initializer_list>
#include <string>
int main() {
const auto* my_data = R"(first line
  indented

last line)";
(void)my_data;
my_data = R"(first line
  indented

last line)";
    (void)my_data;
    return 0;
}

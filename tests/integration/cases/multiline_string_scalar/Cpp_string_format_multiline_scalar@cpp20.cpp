#include <initializer_list>
#include <string>
int main() {
const auto* my_data = R"(
root first line
  indented

root last line
)";
    (void)my_data;
    return 0;
}

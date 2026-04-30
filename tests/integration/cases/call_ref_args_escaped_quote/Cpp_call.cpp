#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
auto process(auto...) { return 0; }
int main() {
const auto* my_str = "a\"b";
process(my_str);
    return 0;
}

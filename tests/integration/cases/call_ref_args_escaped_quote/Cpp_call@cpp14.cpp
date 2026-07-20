#include <initializer_list>
#include <string>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
const auto* my_str = "a\"b";
process(my_str);
    return 0;
}

#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
auto process(auto...) { return 0; }
int main() {
std::string my_str = "a\"b";
process(std::move(my_str));
    return 0;
}

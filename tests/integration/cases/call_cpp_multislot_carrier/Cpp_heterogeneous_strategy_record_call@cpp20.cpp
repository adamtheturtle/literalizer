#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process(1, "hello");
process("two", false);
process(3.5, nullptr);
    return 0;
}

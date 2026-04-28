#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
auto main() -> int {
process("hello");
process(42);
process(true);
    return 0;
}

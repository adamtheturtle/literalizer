#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process(nullptr);
process("hello");
    return 0;
}

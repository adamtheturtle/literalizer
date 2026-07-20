#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
#include <tuple>
auto process(auto...) { return 0; }
int main() {
process("hello");
process(42);
process(true);
    return 0;
}

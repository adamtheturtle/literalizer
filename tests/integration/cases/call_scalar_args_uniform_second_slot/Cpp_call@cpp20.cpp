#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process("hello", "a");
process(42, "b");
process(true, "c");
    return 0;
}

#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
auto emit(auto...) { return 0; }
int main() {
emit(process("hello"), "one");
emit(process(42), "zero");
    return 0;
}

#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
auto emit(auto...) { return 0; }
int main() {
emit(process("hello"), std::map<std::string, int>{{"a", 1}, {"b", 2}});
emit(process(42), std::map<std::string, int>{{"c", 3}, {"d", 4}});
    return 0;
}

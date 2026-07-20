#include <initializer_list>
#include <string>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process("a\"b");
    return 0;
}

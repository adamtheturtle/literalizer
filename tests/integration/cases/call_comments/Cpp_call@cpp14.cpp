#include <initializer_list>
#include <string>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
// Test cases
process("hello");  // single word
process("hello world");  // two words
// trailing comment
    return 0;
}

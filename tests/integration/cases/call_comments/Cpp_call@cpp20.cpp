#include <initializer_list>
#include <string>
#include <vector>
auto process(auto...) { return 0; }
int main() {
// Test cases
process("hello");  // single word
process("hello world");  // two words
// trailing comment
    return 0;
}

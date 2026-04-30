#include <initializer_list>
#include <string>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process("a\"b");
    return 0;
}

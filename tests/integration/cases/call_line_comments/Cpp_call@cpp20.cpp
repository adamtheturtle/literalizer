#include <initializer_list>
#include <string>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process("Dune");  // first edition
process("Solaris");
process("Neuromancer");  // cyberpunk
    return 0;
}

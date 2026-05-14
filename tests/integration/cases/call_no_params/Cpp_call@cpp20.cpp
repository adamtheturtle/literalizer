#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process();
process();
    return 0;
}

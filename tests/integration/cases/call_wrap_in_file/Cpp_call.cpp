#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
auto main() -> int {
process(1, 2);
process(3, 4);
    return 0;
}

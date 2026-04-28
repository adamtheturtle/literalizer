#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
auto main() -> int {
process(1, 42);
process(2, 100);
    return 0;
}

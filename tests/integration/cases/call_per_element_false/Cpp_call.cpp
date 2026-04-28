#include <initializer_list>
auto process(auto...) { return 0; }
auto main() -> int {
process(1);
    return 0;
}

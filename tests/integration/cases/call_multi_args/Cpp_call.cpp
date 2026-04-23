#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
void check_() {
process(1, 42);
process(2, 100);
}

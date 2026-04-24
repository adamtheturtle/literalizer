#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
void check_() {
process(1, 2);
process(3, 4);
}

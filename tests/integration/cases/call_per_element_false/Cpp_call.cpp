#include <initializer_list>
auto process(auto...) { return 0; }
void check_() {
process(1);
}

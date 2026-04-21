#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
void check_() {
(process("hello"));
(process(42));
(process(true));
}

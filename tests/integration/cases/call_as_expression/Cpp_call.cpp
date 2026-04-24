#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
auto process(auto...) { return 0; }
void check_() {
auto items = std::vector<std::nullptr_t>{
process(1, 42),
process(2, 100),
};
    (void)items;
}

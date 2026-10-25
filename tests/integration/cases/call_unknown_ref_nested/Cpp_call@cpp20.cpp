#include <initializer_list>
#include <vector>
#include <type_traits>
auto process(auto...) { return 0; }
int main() {
auto known_value = true;
auto unknown_value = true;
process(known_value, unknown_value);
    return 0;
}

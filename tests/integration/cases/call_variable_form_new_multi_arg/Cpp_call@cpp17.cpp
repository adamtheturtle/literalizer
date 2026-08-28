#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
template <typename... Args> auto record_entry(Args...) { return 0; }
int main() {
auto my_data = record_entry("a", 1, true);
    (void)my_data;
    return 0;
}

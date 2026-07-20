#include <initializer_list>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto my_data = process(1, 2);
    (void)my_data;
    return 0;
}

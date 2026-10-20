#include <initializer_list>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
static auto my_data = process(1);
    (void)my_data;
    return 0;
}

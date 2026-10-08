#include <initializer_list>
#include <vector>
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
auto external_value = 1;
consume(external_value);
    return 0;
}

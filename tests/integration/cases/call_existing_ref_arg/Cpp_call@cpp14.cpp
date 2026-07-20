#include <initializer_list>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto existing = 42;
process(existing);
    return 0;
}

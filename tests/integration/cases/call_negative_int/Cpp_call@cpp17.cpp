#include <initializer_list>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(-1);
process(-2);
process(-3);
    return 0;
}

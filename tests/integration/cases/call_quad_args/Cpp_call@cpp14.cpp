#include <initializer_list>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(1, 2, 3, 4);
process(5, 6, 7, 8);
    return 0;
}

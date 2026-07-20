#include <initializer_list>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(1);
    return 0;
}

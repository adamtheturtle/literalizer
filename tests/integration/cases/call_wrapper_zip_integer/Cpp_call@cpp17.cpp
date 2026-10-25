#include <initializer_list>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
template <typename... Args> auto emit(Args...) { return 0; }
int main() {
emit(process(1), 42);
    return 0;
}

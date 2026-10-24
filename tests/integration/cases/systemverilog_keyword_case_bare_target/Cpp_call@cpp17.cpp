#include <initializer_list>
template <typename... Args> auto Before(Args...) { return 0; }
int main() {
Before(1);
    return 0;
}

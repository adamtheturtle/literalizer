#include <initializer_list>
#include <vector>
template <typename... Args> auto capture(Args...) { return 0; }
int main() {
capture(1);
    return 0;
}

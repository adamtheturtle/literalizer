#include <initializer_list>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
static_cast<void>(process(1));
static_cast<void>(process(2));
    return 0;
}

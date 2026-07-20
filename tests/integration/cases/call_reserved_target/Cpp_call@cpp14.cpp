#include <initializer_list>
#include <string>
#include <vector>
template <typename... Args> auto op(Args...) { return 0; }
int main() {
op("hello");
    return 0;
}

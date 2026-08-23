#include <initializer_list>
#include <string>
#include <vector>
template <typename... Args> auto self(Args...) { return 0; }
int main() {
self("hello");
    return 0;
}

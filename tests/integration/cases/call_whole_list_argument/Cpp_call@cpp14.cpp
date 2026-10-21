#include <initializer_list>
#include <vector>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
f(std::vector<int>{1});
    return 0;
}

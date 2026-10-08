#include <initializer_list>
#include <vector>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
auto ref_data = 1;
f(ref_data);
    return 0;
}

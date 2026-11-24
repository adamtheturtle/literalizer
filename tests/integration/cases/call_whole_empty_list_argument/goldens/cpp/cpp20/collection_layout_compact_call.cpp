#include <cstddef>
#include <vector>
auto f(auto...) { return 0; }
int main() {
f(std::vector<std::nullptr_t>{});
    return 0;
}

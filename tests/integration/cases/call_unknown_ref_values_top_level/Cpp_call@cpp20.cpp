#include <cstddef>
#include <vector>
auto process(auto...) { return 0; }
int main() {
auto unknown_value = std::vector<std::nullptr_t>{};
process(unknown_value);
    return 0;
}

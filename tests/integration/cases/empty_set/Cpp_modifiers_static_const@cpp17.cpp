#include <vector>
#include <cstddef>
int main() {
static const auto my_data = std::vector<std::nullptr_t>{};
    (void)my_data;
    return 0;
}

#include <cstddef>
#include <vector>
int main() {
auto value = nullptr;
auto my_data = std::vector<std::nullptr_t>{
    value,
    value,
    nullptr,
};
    (void)my_data;
    return 0;
}

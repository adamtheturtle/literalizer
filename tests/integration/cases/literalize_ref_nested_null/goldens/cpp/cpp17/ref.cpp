#include <cstddef>
#include <vector>
int main() {
auto my_null = nullptr;
auto my_data = std::vector<std::nullptr_t>{
    my_null,
    nullptr,
};
    (void)my_data;
    return 0;
}

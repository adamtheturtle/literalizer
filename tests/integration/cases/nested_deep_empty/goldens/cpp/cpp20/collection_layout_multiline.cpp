#include <cstddef>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<std::vector<std::nullptr_t>>>{
    std::vector<std::vector<std::nullptr_t>>{
        std::vector<std::nullptr_t>{},
        std::vector<std::nullptr_t>{},
    },
};
    (void)my_data;
    return 0;
}

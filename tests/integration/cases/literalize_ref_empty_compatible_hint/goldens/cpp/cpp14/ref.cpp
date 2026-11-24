#include <cstddef>
#include <vector>
#include <utility>
int main() {
auto record_data = std::vector<std::nullptr_t>{};
auto&& my_data = std::move(record_data);
    (void)my_data;
    return 0;
}

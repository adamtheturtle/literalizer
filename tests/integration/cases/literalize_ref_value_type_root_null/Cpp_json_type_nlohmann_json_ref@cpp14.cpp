#include <nlohmann/json.hpp>
#include <utility>
int main() {
    try {
auto shared = nlohmann::json(nullptr);
auto&& my_data = std::move_if_noexcept(shared);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}

#include <nlohmann/json.hpp>
int main() {
    try {
auto ref_data = nlohmann::json::array({
    1,
    2,
});
auto&& my_data = std::move(ref_data);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}

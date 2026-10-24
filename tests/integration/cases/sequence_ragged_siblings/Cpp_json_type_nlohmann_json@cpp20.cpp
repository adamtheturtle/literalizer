#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    nlohmann::json::array({"set_task", "web", "lint_web"}),
    nlohmann::json::array({"merge_pipelines"}),
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}

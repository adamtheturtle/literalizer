#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    "中中中中中中中中中中中中中中中中中中中中",
    "é'é'é'é'é'é'é'é'é'é'",
    "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂",
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}

#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
    1,
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}

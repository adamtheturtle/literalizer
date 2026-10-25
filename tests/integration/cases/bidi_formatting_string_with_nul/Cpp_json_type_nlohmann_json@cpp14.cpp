#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"v", std::string{'\141', '\342', '\200', '\252', '\000', '\303', '\251', '\360', '\237', '\230', '\200', '\142'}},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}

#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::string, int>>{
    "2000-01-01T01:02:03",
    1,
};
    (void)my_data;
    return 0;
}

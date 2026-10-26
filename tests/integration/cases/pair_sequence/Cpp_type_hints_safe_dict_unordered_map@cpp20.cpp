#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<int, std::string>>{
    1,
    "hello",
};
    (void)my_data;
    return 0;
}

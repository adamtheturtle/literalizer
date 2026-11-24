#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::string, int>>{
    "hello",
    42,
};
    (void)my_data;
    return 0;
}

#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<long, std::string>>{
    1L,
    "hello",
};
    (void)my_data;
    return 0;
}

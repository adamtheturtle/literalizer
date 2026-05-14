#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<long, std::string>>{
    1L,
    "hello",
};
    (void)my_data;
    return 0;
}

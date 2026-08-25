#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::variant<int, std::string>>>{
    std::vector<std::variant<int, std::string>>{2, "hello"},  // trailing note
    // next element
    std::vector<std::variant<int, std::string>>{3, "world"},
};
    (void)my_data;
    return 0;
}

#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record1 { std::vector<bool> k; };
struct Record0 { std::vector<std::variant<int, std::string, std::vector<std::variant<int, std::string>>, Record1>> h; };
int main() {
auto my_data = Record0{
    .h = {
        1,
        "a",
        std::vector<std::variant<int, std::string>>{
            2,
            "b",
        },
        Record1{
            .k = {
                true,
            },
        },
    },
};
    (void)my_data;
    return 0;
}

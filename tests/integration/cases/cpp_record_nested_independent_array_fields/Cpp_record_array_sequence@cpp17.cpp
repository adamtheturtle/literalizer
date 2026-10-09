#include <initializer_list>
#include <string>
#include <array>
#include <variant>
struct Record0 { std::array<std::array<int, 1>, 2> numbers{}; std::array<std::array<std::string, 1>, 2> words; };
int main() {
auto my_data = Record0{
    {
        std::array<int, 1>{
            1,
        },
        std::array<int, 1>{
            2,
        },
    },
    {
        std::array<std::string, 1>{
            "s",
        },
        std::array<std::string, 1>{
            "t",
        },
    },
};
    (void)my_data;
    return 0;
}

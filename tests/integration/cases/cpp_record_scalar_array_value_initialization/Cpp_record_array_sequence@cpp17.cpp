#include <initializer_list>
#include <string>
#include <array>
#include <variant>
struct Record0 { std::array<int, 2> numbers{}; std::array<std::array<int, 2>, 2> nested_numbers{}; std::array<std::string, 1> words; bool flag{}; };
int main() {
auto my_data = Record0{
    {
        1,
        2,
    },
    {
        std::array<int, 2>{
            3,
            4,
        },
        std::array<int, 2>{
            5,
            6,
        },
    },
    {
        "s",
    },
    true,
};
    (void)my_data;
    return 0;
}

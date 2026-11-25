#include <array>
#include <string>
struct Record0 { std::array<bool, 2> flags{}; std::array<double, 2> values{}; std::array<int, 2> ints{}; std::array<std::string, 1> text; std::array<std::array<bool, 1>, 2> nested_flags{}; std::array<std::array<double, 1>, 2> nested_values{}; };
int main() {
auto my_data = Record0{
    {
        true,
        false,
    },
    {
        1.5,
        -2.25,
    },
    {
        1,
        2,
    },
    {
        "a",
    },
    {
        std::array<bool, 1>{
            true,
        },
        std::array<bool, 1>{
            false,
        },
    },
    {
        std::array<double, 1>{
            1.5,
        },
        std::array<double, 1>{
            2.25,
        },
    },
};
    (void)my_data;
    return 0;
}

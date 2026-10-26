#include <string>
#include <vector>
struct Record0 { std::vector<bool> flags; std::vector<double> values; std::vector<int> ints; std::vector<std::string> text; std::vector<std::vector<bool>> nested_flags; std::vector<std::vector<double>> nested_values; };
int main() {
auto my_data = Record0{
    .flags = {
        true,
        false,
    },
    .values = {
        1.5,
        -2.25,
    },
    .ints = {
        1,
        2,
    },
    .text = {
        "a",
    },
    .nested_flags = {
        std::vector<bool>{
            true,
        },
        std::vector<bool>{
            false,
        },
    },
    .nested_values = {
        std::vector<double>{
            1.5,
        },
        std::vector<double>{
            2.25,
        },
    },
};
    (void)my_data;
    return 0;
}

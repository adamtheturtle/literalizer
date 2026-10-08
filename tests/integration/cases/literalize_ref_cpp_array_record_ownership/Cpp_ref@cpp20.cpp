#include <initializer_list>
#include <string>
#include <array>
#include <variant>
struct Record1 { std::array<int, 2> values{}; };
struct Record2 { std::array<std::array<int, 2>, 2> nested{}; };
struct Record0 { Record1 trivial; Record2 nested; };
int main() {
auto trivial = Record1{
    .values = {
        1,
        2,
    },
};
auto nested = Record2{
    .nested = {
        std::array<int, 2>{
            1,
            2,
        },
        std::array<int, 2>{
            3,
            4,
        },
    },
};
auto my_data = Record0{
    .trivial = trivial,
    .nested = nested,
};
    (void)my_data;
    return 0;
}

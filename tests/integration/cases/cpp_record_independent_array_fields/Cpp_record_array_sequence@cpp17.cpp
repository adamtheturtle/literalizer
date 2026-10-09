#include <initializer_list>
#include <string>
#include <array>
#include <variant>
struct Record0 { std::array<int, 1> numbers{}; std::array<std::string, 1> words; };
int main() {
auto my_data = Record0{
    {
        1,
    },
    {
        "s",
    },
};
    (void)my_data;
    return 0;
}

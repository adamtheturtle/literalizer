#include <initializer_list>
#include <string>
#include <array>
#include <variant>
struct Record0 { std::array<std::string, 1> labels; };
int main() {
auto first = Record0{
    {
        "owned",
    },
};
auto my_data = std::move(first);
    (void)my_data;
    return 0;
}

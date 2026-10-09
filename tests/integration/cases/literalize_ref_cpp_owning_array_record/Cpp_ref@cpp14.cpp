#include <initializer_list>
#include <string>
#include <array>
struct Record0 { std::array<std::string, 1> labels; };
#include <utility>
int main() {
auto first = Record0{
    {
        "owned",
    },
};
auto&& my_data = std::move(first);
    (void)my_data;
    return 0;
}

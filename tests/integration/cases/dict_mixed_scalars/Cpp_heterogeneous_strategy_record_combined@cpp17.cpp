#include <initializer_list>
#include <string>
#include <map>
#include <variant>
struct Record0 { int a{}; std::string b; };
int main() {
auto my_data = Record0{
    1,
    "x",
};
(void)my_data;
my_data = Record0{
    1,
    "x",
};
    (void)my_data;
    return 0;
}

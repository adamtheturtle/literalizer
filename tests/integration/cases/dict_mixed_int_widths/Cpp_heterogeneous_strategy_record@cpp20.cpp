#include <initializer_list>
#include <string>
#include <map>
#include <variant>
struct Record0 { int a{}; long long b{}; std::string c; };
int main() {
auto my_data = Record0{
    .a = 1,
    .b = 3000000000,
    .c = "x",
};
    (void)my_data;
    return 0;
}

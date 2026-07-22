#include <initializer_list>
#include <string>
#include <map>
struct Record0 { int a{}; long long b{}; std::string c; };
int main() {
auto my_data = Record0{
    1,
    3000000000,
    "x",
};
    (void)my_data;
    return 0;
}

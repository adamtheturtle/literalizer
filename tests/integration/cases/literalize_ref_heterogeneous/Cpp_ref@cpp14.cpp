#include <initializer_list>
#include <string>
#include <map>
struct Record0 { int a{}; std::string b; };
int main() {
auto my_data = Record0{
    1,
    "hello",
};
    (void)my_data;
    return 0;
}

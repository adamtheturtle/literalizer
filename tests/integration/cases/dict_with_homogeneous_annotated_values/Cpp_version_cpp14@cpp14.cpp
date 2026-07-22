#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct Record0 { std::vector<std::nullptr_t> a; std::vector<std::nullptr_t> b; };
int main() {
auto my_data = Record0{
    std::vector<std::nullptr_t>{},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}

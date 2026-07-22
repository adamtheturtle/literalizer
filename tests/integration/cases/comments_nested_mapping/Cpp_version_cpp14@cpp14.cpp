#include <initializer_list>
#include <string>
#include <map>
struct Record0 { std::map<std::string, int> a; int b{}; };
int main() {
auto my_data = Record0{
    std::map<std::string, int>{
        {"x", 1},
    },
    2,
};
    (void)my_data;
    return 0;
}

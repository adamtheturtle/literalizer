#include <initializer_list>
#include <string>
#include <map>
struct Record0 { std::string name; int port{}; };
int main() {
auto my_data = Record0{
    // Configuration
    "app",
    // Port setting
    3000,
};
    (void)my_data;
    return 0;
}

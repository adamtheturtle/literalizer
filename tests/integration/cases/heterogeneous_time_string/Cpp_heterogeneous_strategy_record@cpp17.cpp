#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct Record0 { std::vector<std::string> vals; };
int main() {
auto my_data = Record0{
    .vals = std::vector<std::string>{
        "09:30:00",
        "hello",
    },
};
    (void)my_data;
    return 0;
}

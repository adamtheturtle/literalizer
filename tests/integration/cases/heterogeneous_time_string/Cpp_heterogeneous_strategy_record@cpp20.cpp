#include <initializer_list>
#include <string>
#include <vector>
struct Record0 { std::vector<std::string> vals; };
int main() {
auto my_data = Record0{
    .vals = {
        "09:30:00",
        "hello",
    },
};
    (void)my_data;
    return 0;
}

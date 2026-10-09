#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long>{
    {"minimum", -2147483648L},
    {"below", -3000000000L},
};
    (void)my_data;
    return 0;
}

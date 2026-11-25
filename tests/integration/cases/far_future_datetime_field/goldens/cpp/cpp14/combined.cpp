#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"ts", "3000-12-31T23:59:59.999999+00:00"},
};
(void)my_data;
my_data = std::map<std::string, std::string>{
    {"ts", "3000-12-31T23:59:59.999999+00:00"},
};
    (void)my_data;
    return 0;
}

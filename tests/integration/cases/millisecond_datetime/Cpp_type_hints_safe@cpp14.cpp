#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"half", "1979-05-27T07:32:00.500000"},
    {"milli", "1979-05-27T07:32:00.100000"},
    {"max_milli", "1979-05-27T07:32:00.999000"},
    {"whole", "1979-05-27T07:32:00"},
};
    (void)my_data;
    return 0;
}

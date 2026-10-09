#include <initializer_list>
#include <string>
#include <map>
int main() {
auto text = std::string{'\141', '\342', '\200', '\252', '\142'};
auto my_data = std::map<std::string, std::string>{
    {"value", std::move(text)},
};
    (void)my_data;
    return 0;
}

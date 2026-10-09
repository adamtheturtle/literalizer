#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"v", std::string{'\141', '\342', '\200', '\252', '\000', '\303', '\251', '\360', '\237', '\230', '\200', '\142'}},
};
    (void)my_data;
    return 0;
}

#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"v", std::string{'\141', '\342', '\200', '\252', '\342', '\200', '\253', '\342', '\200', '\254', '\342', '\200', '\255', '\342', '\200', '\256', '\342', '\201', '\246', '\342', '\201', '\247', '\342', '\201', '\250', '\342', '\201', '\251', '\142'}},
};
    (void)my_data;
    return 0;
}

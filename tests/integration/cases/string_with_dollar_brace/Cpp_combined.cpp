#include <initializer_list>
#include <string>
#include <vector>
void check_() {
auto my_data = std::vector<std::string>{
    "prefix ${HOME} suffix",
    "${interpolated}",
};
(void)my_data;
my_data = std::vector<std::string>{
    "prefix ${HOME} suffix",
    "${interpolated}",
};
    (void)my_data;
}

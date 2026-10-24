#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::string, int>>{
    "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
    1,
};
    (void)my_data;
    return 0;
}

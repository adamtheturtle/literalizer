#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::string, int>>{
    R"(This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.)",
    1,
};
    (void)my_data;
    return 0;
}

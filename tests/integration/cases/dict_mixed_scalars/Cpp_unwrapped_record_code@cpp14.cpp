#include <vector>
#include <string>
struct Record0 { int a{}; std::string b; };
int main() {

    auto my_data = std::vector<Record0>{Record0{
    1,
    "x",
}};
    (void)my_data;
    return 0;
}

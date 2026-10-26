#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    {R"(x)", "line1\r\nline2"},
};
    (void)my_data;
    return 0;
}

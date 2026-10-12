#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {R"(x)", R"(﻿)"},
};
    (void)my_data;
    return 0;
}

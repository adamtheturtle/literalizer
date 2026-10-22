#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<std::string>>{
    std::vector<std::string>{"set_task", "web", "lint_web"},
    std::vector<std::string>{"merge_pipelines"},
};
    (void)my_data;
    return 0;
}

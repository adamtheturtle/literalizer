#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    "中中中中中中中中中中中中中中中中中中中中",
    "é'é'é'é'é'é'é'é'é'é'",
    "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂",
};
(void)my_data;
my_data = std::vector<std::string>{
    "中中中中中中中中中中中中中中中中中中中中",
    "é'é'é'é'é'é'é'é'é'é'",
    "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂",
};
    (void)my_data;
    return 0;
}

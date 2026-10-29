#include <nlohmann/json.hpp>
struct objType_ { void std(auto...) const {} };
const objType_ obj;
int main() {
    try {
obj.std(nlohmann::json(1));
        return 0;
    } catch (...) {
        return 1;
    }
}

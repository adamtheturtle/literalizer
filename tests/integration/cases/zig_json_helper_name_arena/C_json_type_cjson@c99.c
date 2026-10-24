#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n0, "a", _n1);
cJSON *arena = _n0;
    (void)arena;
    return 0;
}

#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n0, "a", _n1);
cJSON *ZKV = _n0;
    (void)ZKV;
    return 0;
}

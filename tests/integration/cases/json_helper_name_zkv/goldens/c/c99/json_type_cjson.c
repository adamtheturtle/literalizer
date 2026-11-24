#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_ZKV_n0 = cJSON_CreateObject();
cJSON *literalizer_ZKV_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(literalizer_ZKV_n0, "a", literalizer_ZKV_n1);
cJSON *ZKV = literalizer_ZKV_n0;
    (void)ZKV;
    return 0;
}

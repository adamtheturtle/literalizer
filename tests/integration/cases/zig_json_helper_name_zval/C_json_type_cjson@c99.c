#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_ZVal_n0 = cJSON_CreateObject();
cJSON *literalizer_ZVal_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(literalizer_ZVal_n0, "a", literalizer_ZVal_n1);
cJSON *ZVal = literalizer_ZVal_n0;
    (void)ZVal;
    return 0;
}

#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_userObj_n0 = cJSON_CreateObject();
cJSON *literalizer_userObj_n1 = cJSON_CreateString("_");
cJSON_AddItemToObject(literalizer_userObj_n0, "_", literalizer_userObj_n1);
cJSON *userObj = literalizer_userObj_n0;
cJSON * my_data = userObj;
    (void)my_data;
    return 0;
}

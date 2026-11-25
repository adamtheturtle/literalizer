#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateArray();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("1901-12-13T20:45:51Z");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateString("1901-12-13T20:45:52Z");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateString("2038-01-19T03:14:07Z");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n3);
cJSON *literalizer_my_data_n4 = cJSON_CreateString("2038-01-19T03:14:08Z");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n4);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}

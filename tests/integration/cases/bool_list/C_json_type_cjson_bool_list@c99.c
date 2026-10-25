#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateArray();
cJSON *literalizer_my_data_n1 = cJSON_CreateBool(1);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateBool(0);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateBool(1);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n3);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}

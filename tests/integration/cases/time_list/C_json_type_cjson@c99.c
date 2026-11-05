#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateArray();
cJSON *literalizer_my_data_n2 = cJSON_CreateString("09:30:00");
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateString("17:45:00");
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n3);
cJSON *literalizer_my_data_n4 = cJSON_CreateString("23:59:59");
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n4);
cJSON_AddItemToObject(literalizer_my_data_n0, "times", literalizer_my_data_n1);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}

#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_shared_n5 = cJSON_CreateNumber((double)42);
cJSON *shared = literalizer_shared_n5;
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateArray();
cJSON *literalizer_my_data_n2 = cJSON_Duplicate(shared, 1);
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_Duplicate(shared, 1);
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n3);
cJSON_AddItemToObject(literalizer_my_data_n0, "refs", literalizer_my_data_n1);
cJSON *literalizer_my_data_n4 = cJSON_CreateString("#{shared}");
cJSON_AddItemToObject(literalizer_my_data_n0, "quoted", literalizer_my_data_n4);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}

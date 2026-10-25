#include <cjson/cJSON.h>
int main(void) {
        cJSON *literalizer_shared_n4 = cJSON_CreateArray();
cJSON *literalizer_shared_n5 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(literalizer_shared_n4, literalizer_shared_n5);
cJSON *literalizer_shared_n6 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(literalizer_shared_n4, literalizer_shared_n6);
cJSON *shared = literalizer_shared_n4;
        cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateObject();
cJSON *literalizer_my_data_n2 = cJSON_Duplicate(shared, 1);
cJSON_AddItemToObject(literalizer_my_data_n1, "nested", literalizer_my_data_n2);
cJSON_AddItemToObject(literalizer_my_data_n0, "field", literalizer_my_data_n1);
cJSON *literalizer_my_data_n3 = cJSON_CreateString("first\n{ \" // }");
cJSON_AddItemToObject(literalizer_my_data_n0, "text", literalizer_my_data_n3);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}

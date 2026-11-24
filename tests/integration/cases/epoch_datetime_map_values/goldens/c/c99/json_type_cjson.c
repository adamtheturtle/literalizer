#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("2024-01-15T12:00:00Z");
cJSON_AddItemToObject(literalizer_my_data_n0, "within_i32", literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateString("2099-06-15T08:30:00Z");
cJSON_AddItemToObject(literalizer_my_data_n0, "beyond_i32", literalizer_my_data_n2);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}

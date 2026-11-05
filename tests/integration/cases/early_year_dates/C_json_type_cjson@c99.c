#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("0099-05-27");
cJSON_AddItemToObject(literalizer_my_data_n0, "date", literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateString("0001-01-01T12:30:00Z");
cJSON_AddItemToObject(literalizer_my_data_n0, "naive", literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateString("2024-05-27T10:00:00Z");
cJSON_AddItemToObject(literalizer_my_data_n0, "recent", literalizer_my_data_n3);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}

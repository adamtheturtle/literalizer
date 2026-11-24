#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("2024-01-15");
cJSON_AddItemToObject(literalizer_my_data_n0, "date", literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateString("2024-01-15T12:30:00+00:00");
cJSON_AddItemToObject(literalizer_my_data_n0, "datetime", literalizer_my_data_n2);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}

#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("09:30:00");
cJSON_AddItemToObject(literalizer_my_data_n0, "morning", literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateString("14:15:00");
cJSON_AddItemToObject(literalizer_my_data_n0, "afternoon", literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateString("23:59:59");
cJSON_AddItemToObject(literalizer_my_data_n0, "evening", literalizer_my_data_n3);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}

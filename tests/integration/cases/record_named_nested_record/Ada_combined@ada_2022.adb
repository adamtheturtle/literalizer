with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("project", AStr ("alpha")),
        AEntry ("lead_item", AMap'[AEntry ("id", AInt (100)), AEntry ("label", AStr ("first item")), AEntry ("enabled", ABool (False)), AEntry ("related_ids", AList'[AInt (102), AInt (103)])])
    ];
begin
    my_data := AMap'[
        AEntry ("project", AStr ("alpha")),
        AEntry ("lead_item", AMap'[AEntry ("id", AInt (100)), AEntry ("label", AStr ("first item")), AEntry ("enabled", ABool (False)), AEntry ("related_ids", AList'[AInt (102), AInt (103)])])
    ];
end Main;

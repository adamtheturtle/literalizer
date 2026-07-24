with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("collection", AStr ("alpha")),
        AEntry ("featured_entry", AMap'[AEntry ("id", AInt (100)), AEntry ("label", AStr ("first entry")), AEntry ("enabled", ABool (False)), AEntry ("related_ids", AList'[AInt (102), AInt (103)])])
    ];
begin
    my_data := AMap'[
        AEntry ("collection", AStr ("alpha")),
        AEntry ("featured_entry", AMap'[AEntry ("id", AInt (100)), AEntry ("label", AStr ("first entry")), AEntry ("enabled", ABool (False)), AEntry ("related_ids", AList'[AInt (102), AInt (103)])])
    ];
end Main;

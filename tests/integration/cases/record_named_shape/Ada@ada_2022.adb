with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("id", AInt (100)), AEntry ("label", AStr ("first item")), AEntry ("enabled", ABool (False)), AEntry ("related_ids", AList'[AInt (102), AInt (103)])],
        AMap'[AEntry ("id", AInt (101)), AEntry ("label", AStr ("second item")), AEntry ("enabled", ABool (True)), AEntry ("related_ids", AList'[AInt (100)])]
    ];
begin
    null;
end Main;

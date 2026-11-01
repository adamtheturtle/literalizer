with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("ancient_date", AStr ("1500-03-01")),
        AEntry ("modern_date", AStr ("2024-01-15")),
        AEntry ("before_date", AStr ("1582-10-04")),
        AEntry ("gap_date", AStr ("1582-10-10")),
        AEntry ("transition_date", AStr ("1582-10-15")),
        AEntry ("after_date", AStr ("1582-10-16")),
        AEntry ("before_naive", AStr ("1582-10-04T12:30:00.000001")),
        AEntry ("gap_naive", AStr ("1582-10-10T12:30:00.500000")),
        AEntry ("transition_positive", AStr ("1582-10-15T00:30:00+18:00")),
        AEntry ("transition_negative", AStr ("1582-10-15T23:30:00-18:00")),
        AEntry ("after_positive", AStr ("1582-10-16T00:30:00+18:00"))
    ];
begin
    null;
end Main;

with A_Stub; use A_Stub;
procedure Main is
    procedure Check (Timestamp : A_Val; Date_Value : A_Val) is begin null; end Check;
begin
    Check(timestamp => AStr ("2024-01-15T10:30:00+00:00"), date_value => AStr ("2024-06-01"));
end Main;

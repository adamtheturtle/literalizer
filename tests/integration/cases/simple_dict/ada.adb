procedure Check is
   X : Integer := AMap'(
       AEntry ("name", AStr ("Alice")),
       AEntry ("age", AInt (30)),
       AEntry ("active", ABool (True)),
       AEntry ("score", ANull)
   );
begin
   null;
end Check;

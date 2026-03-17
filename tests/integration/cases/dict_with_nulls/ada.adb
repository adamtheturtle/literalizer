procedure Check is
   X : Integer := AMap'(
       AEntry ("name", AStr ("Alice")),
       AEntry ("score", ANull),
       AEntry ("age", AInt (30))
   );
begin
   null;
end Check;

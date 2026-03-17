procedure Check is
   X : Integer := AList'(
       ABool (True),
       AStr ("hi"),
       AList'(AInt (1), AInt (2)),
       ANull
   );
begin
   null;
end Check;

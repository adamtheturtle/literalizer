Imports System.Collections.Generic
Class Counter
    Public calls As Integer
    Public Function accept(user As String, timestamp As Double) As Boolean
        If user <> If(calls = 0, "user_1", "user_2") OrElse timestamp <> 100.0 + calls Then Throw New System.Exception("receiver arguments changed")
        calls += 1
        Return user = "user_1"
    End Function
End Class
Module Check
    Dim checks As Integer
    Sub checkResult(actual As Boolean, expected As Object())
        If actual <> CBool(expected(0)) OrElse CStr(expected(1)) <> If(checks = 0, "first", "second") Then Throw New System.Exception("paired result changed")
        checks += 1
    End Sub
    Sub Main()
        Dim counter As New Counter()
        checkResult(counter.accept("user_1", 100.0), New Object() {True, "first"})
        If counter.calls <> 1 OrElse checks <> 1 Then Throw New System.Exception("calls skipped")
    End Sub
End Module

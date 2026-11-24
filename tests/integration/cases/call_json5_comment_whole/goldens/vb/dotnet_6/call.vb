Imports System.Collections.Generic
Module Check
    Dim eventIndex As Integer
    Sub ObserveEvent(actual As Long)
        Dim expected As Long() = {1, 42}
        If eventIndex >= 2 OrElse actual <> expected(eventIndex) Then Throw New System.Exception("receiver event changed")
        eventIndex += 1
    End Sub
    Function f(a As Long) As Long
        ObserveEvent(1) : ObserveEvent(a)
        Return a + 100
    End Function
    Private Sub verify_events()
        If eventIndex <> 2 Then Throw New System.Exception("missing receiver events")
    End Sub
    Sub _calls()
        ' scalar heading
        ' second heading line
        ' scalar inline
        ' inline continuation
        ' scalar trailing
        f(42)
        verify_events()
    End Sub
End Module

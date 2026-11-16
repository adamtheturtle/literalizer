Imports System.Collections.Generic
Module Check
    Dim eventIndex As Integer
    Sub ObserveEvent(actual As Long)
        Dim expected As Long() = {1, -1, 1, -2, 1, -3}
        If eventIndex >= 6 OrElse actual <> expected(eventIndex) Then Throw New System.Exception("receiver event changed")
        eventIndex += 1
    End Sub
    Function process(value As Long) As Long
        ObserveEvent(1) : ObserveEvent(value)
        Return value + 100
    End Function
    Private Sub verify_events()
        If eventIndex <> 6 Then Throw New System.Exception("missing receiver events")
    End Sub
    Sub _calls()
        process(-1)
        process(-2)
        process(-3)
        verify_events()
    End Sub
End Module

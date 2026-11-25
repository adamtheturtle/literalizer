Imports System.Collections.Generic
Module Check
    Dim eventIndex As Integer
    Sub ObserveEvent(actual As Long)
        Dim expected As Long() = {1, 1, 2, 101, 3, 42}
        If eventIndex >= 6 OrElse actual <> expected(eventIndex) Then Throw New System.Exception("receiver event changed")
        eventIndex += 1
    End Sub
    Function process(value As Long) As Long
        ObserveEvent(1) : ObserveEvent(value)
        Return value + 100
    End Function
    Sub emit(actual As Long, zipped As Long)
        ObserveEvent(2) : ObserveEvent(actual)
        ObserveEvent(3) : ObserveEvent(zipped)
    End Sub
    Private Sub verify_events()
        If eventIndex <> 6 Then Throw New System.Exception("missing receiver events")
    End Sub
    Sub _calls()
        emit(process(1), 42)
        verify_events()
    End Sub
End Module

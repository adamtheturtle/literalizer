Imports System.Collections.Generic
Module Check
    Dim eventIndex As Integer
    Sub ObserveEvent(actual As Long)
        Dim expected As Long() = {1, 42, 2, 142}
        If eventIndex >= 4 OrElse actual <> expected(eventIndex) Then Throw New System.Exception("receiver event changed")
        eventIndex += 1
    End Sub
    Function make_widget(value As Long) As Long
        ObserveEvent(1) : ObserveEvent(value)
        Return value + 100
    End Function
    Sub consume(value As Long)
        ObserveEvent(2) : ObserveEvent(value)
    End Sub
    Private Sub verify_events()
        If eventIndex <> 4 Then Throw New System.Exception("missing receiver events")
    End Sub
    Sub _calls()
        Dim my_data = make_widget(42)
        consume(my_data)
        verify_events()
    End Sub
End Module

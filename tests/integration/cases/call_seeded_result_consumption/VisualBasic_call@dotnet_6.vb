Imports System.Collections.Generic
Module Check
    Dim eventIndex As Integer
    Sub ObserveEvent(actual As Long)
        Dim expected As Long() = {2, 0, 1, 1, 2, 101}
        If eventIndex >= 6 OrElse actual <> expected(eventIndex) Then Throw New System.Exception("receiver event changed")
        eventIndex += 1
    End Sub
    Function make_widget(count As Long) As Long
        ObserveEvent(1) : ObserveEvent(count)
        Return count + 100
    End Function
    Sub consume_widget(count As Long)
        ObserveEvent(2) : ObserveEvent(count)
    End Sub
    Private Sub verify_events()
        If eventIndex <> 6 Then Throw New System.Exception("missing receiver events")
    End Sub
    Sub _calls()
        Dim my_data = 0
        consume_widget(my_data)
        my_data = make_widget(1)
        consume_widget(my_data)
        verify_events()
    End Sub
End Module

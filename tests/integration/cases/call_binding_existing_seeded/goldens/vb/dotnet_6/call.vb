Imports System.Collections.Generic
Module Check
    Dim eventIndex As Integer
    Sub ObserveEvent(actual As Long)
        Dim expected As Long() = {1, 42, 1, 42, 1, 142}
        If eventIndex >= 6 OrElse actual <> expected(eventIndex) Then Throw New System.Exception("receiver event changed")
        eventIndex += 1
    End Sub
    Function make_widget(count As Long) As Long
        ObserveEvent(1) : ObserveEvent(count)
        Return count + 100
    End Function
    Private Sub verify_events()
        If eventIndex <> 6 Then Throw New System.Exception("missing receiver events")
    End Sub
    Sub _calls()
        Dim my_data = 42
        make_widget(my_data)
        my_data = make_widget(my_data)
        make_widget(my_data)
        verify_events()
    End Sub
End Module

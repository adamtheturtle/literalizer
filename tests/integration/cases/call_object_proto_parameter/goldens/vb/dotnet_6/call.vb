Imports System.Collections.Generic
Module Check
    Dim eventIndex As Integer
    Sub ObserveEvent(actual As Long)
        Dim expected As Long() = {1, 1}
        If eventIndex >= 2 OrElse actual <> expected(eventIndex) Then Throw New System.Exception("receiver event changed")
        eventIndex += 1
    End Sub
    Function capture(__proto__ As Long) As Long
        ObserveEvent(1) : ObserveEvent(__proto__)
        Return __proto__ + 100
    End Function
    Private Sub verify_events()
        If eventIndex <> 2 Then Throw New System.Exception("missing receiver events")
    End Sub
    Sub _calls()
        capture(1)
        verify_events()
    End Sub
End Module

Sub video_output()
    ActivePresentation.CreateVideo FileName:="output.mp4", _
    UseTimingsAndNarrations:=True, _
    VertResolution:=2160, _
    FramesPerSecond:=60, _
    Quality:=100
End Sub

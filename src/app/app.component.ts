import { Component, OnDestroy } from '@angular/core';
import { AudioRecordingService } from 'src/app/services/audio-recording.service';
import { DomSanitizer } from '@angular/platform-browser';
import { DataService } from './services/data.service';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnDestroy {

  isRecording = false;
  recordedTime;
  blobUrl;
  blob;
  constructor(private audioRecordingService: AudioRecordingService, private sanitizer: DomSanitizer,private dataService:DataService) {

    this.audioRecordingService.recordingFailed().subscribe(() => {
      this.isRecording = false;
    });

    this.audioRecordingService.getRecordedTime().subscribe((time) => {
      this.recordedTime = time;
    });

    this.audioRecordingService.getRecordedBlob().subscribe((data) => {
      this.blob = data.blob;
      this.blobUrl = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(data.blob));
    });
    


  }

  startRecording() {
    if (!this.isRecording) {
      this.isRecording = true;
      this.audioRecordingService.startRecording();
    }
  }

  abortRecording() {
    if (this.isRecording) {
      this.isRecording = false;
      this.audioRecordingService.abortRecording();
    }
  }

  stopRecording() {
    if (this.isRecording) {
      this.audioRecordingService.stopRecording();
      this.isRecording = false;
    }
  }

  clearRecordedData() {
    this.blobUrl = null;
  }
  sendAudio(){
    this.dataService.saveAudio(this.blob).subscribe(()=>{
  
    });
  }

  ngOnDestroy(): void {
    this.abortRecording();
  }

}



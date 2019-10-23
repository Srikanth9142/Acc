import { Component, OnDestroy } from '@angular/core';
import { AudioRecordingService } from 'src/app/services/audio-recording.service';
import { DomSanitizer } from '@angular/platform-browser';
import { DataService } from './services/data.service';
import { Prediction } from 'src/app/models/prediction';
import { take } from 'rxjs/operators';

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
  selected=0;
  send_blob=false;
  predictions : Prediction[];
  predictionValues=false;
  rand=0;
  prediction_modified:any;
  Accents=['Indian','US-Male','US-Female','British','Mild Generic Indian','Mild Hindi','Mild Tamil','Neutral Indian','Strong Bengali','Strong Hindi','Strong Tamil','Strong Telugu'];
  passages = [`I walked along the winding trail,
  the dog running before me,
  my wife next to me,
  with cliffs to one side,
  and a river to the other.
  Tall grasses, as tall as me,
  and evergreen trees, everywhere.
  The wind blew gentle,
  as grey clouds drifted by,
  and I pondered existence.`,
`Temperatures rose, sea level too.
Melting glaciers flooded more land.
Some struggled to reduce emissions.
Others shrugged, undaunted by growing evidence
Of fires, floods, and environmental chaos.`,
`The cat walks away, padding across the floor, its rough tongue sanding the red around its chops. Behind it, the pigeon lies in a carpet of feathers, waiting for the cleaning lady to sweep her lifeless body into the big blue dustbin. In a nest, two eggs wait for warmth.`,`She had attempted to ignore him, hoping he wouldn’t approach her as she stood alone in the aisle of the bookstore. He was the persistent kind, though.

After approaching her, he mustered a polite smile and blinked twice.

“Excuse me,” she said by way of introduction, gently fanning behind herself.`,`A mummy works Macy’s gift wrap counter. He told the boss he has 2,000 years in wrapping. Sometimes his hands get confused and he realizes he’s using bandages from his arm. Unspools. Starts over. Customers curse, but he isn’t bothered by curses, and he has all the time in the world.
`,`“When will I see mommy?” Clare would ask everyday.

“Before you head to bed, honey” Auntie would reply.

Those words echoed in her ear as her eyes pleaded to be closed.

This time,her mother made it. Just before the monitor flat-lined.

Melancholy spread as Clare finally slept with a smile.

`,`She had attempted to ignore him, hoping he wouldn’t approach her as she stood alone in the aisle of the bookstore. He was the persistent kind, though.

After approaching her, he mustered a polite smile and blinked twice.

“Excuse me,” she said by way of introduction, gently fanning behind herself.

`]
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
    this.send_blob=false;
  }
  getReport():void{
    var prediction_modified_str = this.predictions[this.predictions.length-1];
    this.prediction_modified = prediction_modified_str.toString().split("\n");
    console.log(typeof this.prediction_modified);
    console.log(this.prediction_modified);
  }
  getprediction():void{
    this.dataService.get_prediction().pipe(take(1)).subscribe(d =>{
      this.predictions = d;
      this.predictionValues=true;
      
    })
  }

  sendAudio(){
    this.dataService.saveAudio(this.blob,this.selected).subscribe(()=>{
      this.send_blob=true;
      
    });
  }

  ngOnDestroy(): void {
    this.abortRecording();
  }

  getrandom():void{
    this.rand = Math.floor(Math.random()*6+1);
  }

}



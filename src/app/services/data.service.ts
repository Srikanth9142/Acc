import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Prediction } from '../models/prediction';
import {map} from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  constructor(private http:HttpClient) { }
  saveAudio(data:any): any {
    return this.http.post('http://127.0.0.1:8000/accent/save',data,
       {
          headers: {
             "Content-Type": 'application/octet-stream'
          }
       });
 }

 get_prediction():Observable<Prediction[]> {
     console.log("In Data Service");
     return this.http.get<Prediction[]>(
      `${environment.serverurl}/accent/prediction`).pipe(
      map(a => a.map(t=>{return new Prediction(t.prediction)})
      )
   );
  }
}



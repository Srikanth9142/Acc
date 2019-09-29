import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http:HttpClient) { }
  saveAudio(data: any): any {
    return this.http.post('http://127.0.0.1:8000/accent/save', data,
       {
          headers: {
             "Content-Type": 'application/octet-stream'
          }
       });
 }
}



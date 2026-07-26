import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Trade } from './models/trade.model';

@Injectable({
  providedIn: 'root',
})
export class TradeStreamService {
  private socket$: WebSocketSubject<Trade> = webSocket('ws://localhost:8000/ws');
  trade$ = this.socket$.asObservable();
}

import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Trade } from './models/trade.model';
import { map, Observable } from 'rxjs';
import { RawTrade } from './models/trade-raw.model';

@Injectable({
  providedIn: 'root',
})
export class TradeStreamService {
  private socket$: WebSocketSubject<any> = webSocket('ws://localhost:8000/ws');
  
  trade$: Observable<Trade> = this.socket$.asObservable()
    .pipe(map((payload: RawTrade) => ({
      symbol: payload.symbol,
      price: +payload.price,
      quantity: +payload.quantity
    })));

  updateSubscription(symbols: string[]) {
    this.socket$.next({ symbols })
  }
}

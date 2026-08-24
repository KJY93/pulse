import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Trade } from './models/trade.model';
import { filter, map, Observable } from 'rxjs';
import { RawTrade } from './models/trade-raw.model';

@Injectable({
  providedIn: 'root',
})
export class TradeStreamService {
  private socket$: WebSocketSubject<any> = webSocket('ws://localhost:8000/ws');

  trade$: Observable<Trade> = this.socket$.asObservable()
    .pipe(
      filter((payload: any) => !('error' in payload)),
      map((payload: RawTrade) => ({
        symbol: payload.symbol,
        price: +payload.price,
        quantity: +payload.quantity
      })));

  updateSubscription(symbols: string[]) {
    this.socket$.next({ symbols })
  }

  rateLimitNotification$: Observable<{ error: string, message: string }> = this.socket$.asObservable()
    .pipe(
      filter((payload: any) => {
        const isNotice = 'error' in payload;
        return isNotice;
      })
    )
}

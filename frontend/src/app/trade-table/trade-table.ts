import { Component } from '@angular/core';
import { TradeStreamService } from '../trade-stream';
import { inject } from '@angular/core';
import { TradeRow } from '../models/trade-row.model';
import { scan } from 'rxjs/operators';

@Component({
  selector: 'app-trade-table',
  imports: [],
  templateUrl: './trade-table.html',
  styleUrl: './trade-table.css',
})
export class TradeTable {
  private tradeStreamService = inject(TradeStreamService);
  private table$ = this.tradeStreamService.trade$.pipe(
    scan((acc, curr) => {
      const existing = acc[curr.symbol];
      const prevPrice = existing ? existing.currentPrice : curr.price;
      const newRow: TradeRow = {
        symbol: curr.symbol,
        currentPrice: curr.price,
        prevPrice: prevPrice,
        delta: curr.price - prevPrice,
        quantity: curr.quantity,
      };
      return { ...acc, [curr.symbol]: newRow };
    }, {} as Record<string, TradeRow>)
  )
}

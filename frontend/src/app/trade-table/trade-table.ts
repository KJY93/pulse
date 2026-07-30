import { Component, computed } from '@angular/core';
import { TradeStreamService } from '../trade-stream';
import { inject } from '@angular/core';
import { TradeRow } from '../models/trade-row.model';
import { scan, auditTime } from 'rxjs/operators';
import { toSignal } from '@angular/core/rxjs-interop';
import { scanTradeTable } from '../trade-table.logic';

@Component({
  selector: 'app-trade-table',
  imports: [],
  templateUrl: './trade-table.html',
  styleUrl: './trade-table.css',
})
export class TradeTable {
  private tradeStreamService = inject(TradeStreamService);
  private table$ = this.tradeStreamService.trade$.pipe(
    scan(scanTradeTable, {} as Record<string, TradeRow>),
    auditTime(500)
  );
  
  private tradeTableSignal = toSignal(this.table$, {
    initialValue: {} as Record<string, TradeRow> 
  });

  tradeTableSignalArray = computed<TradeRow[]>(() => Object.values(this.tradeTableSignal()));
}

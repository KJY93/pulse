import {
  Component,
  computed,
  Signal,
  signal,
  WritableSignal,
  ChangeDetectionStrategy,
} from '@angular/core';
import { TradeStreamService } from '../trade-stream';
import { inject } from '@angular/core';
import { TradeRow } from '../models/trade-row.model';
import { scan, auditTime } from 'rxjs/operators';
import { toSignal } from '@angular/core/rxjs-interop';
import { scanTradeTable } from '../trade-table.logic';
import { SYMBOLS } from '../symbols';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-trade-table',
  imports: [],
  templateUrl: './trade-table.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrl: './trade-table.css',
})
export class TradeTable {
  availableSymbols: string[] = SYMBOLS;
  checkedSymbols: WritableSignal<Set<string>> = signal<Set<string>>(new Set(this.availableSymbols));
  private tradeStreamService: TradeStreamService = inject(TradeStreamService);
  private table$: Observable<Record<string, TradeRow>> = this.tradeStreamService.trade$.pipe(
    scan(scanTradeTable, {} as Record<string, TradeRow>),
    auditTime(500),
  );

  private tradeTableSignal = toSignal(this.table$, {
    initialValue: {} as Record<string, TradeRow>,
  });

  tradeTableSignalArray: Signal<TradeRow[]> = computed<TradeRow[]>(() =>
    Object.values(this.tradeTableSignal()).filter((row) => this.checkedSymbols().has(row.symbol)),
  );

  onCheckBoxChange(symbol: string, event: Event) {
    const isChecked = (event.target as HTMLInputElement).checked;

    this.checkedSymbols.update((currentSet) => {
      const updated = new Set(currentSet);
      if (isChecked) {
        updated.add(symbol);
      } else {
        updated.delete(symbol);
      }
      return updated;
    });

    this.tradeStreamService.updateSubscription(Array.from(this.checkedSymbols()));
  }
}

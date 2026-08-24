import {
  Component,
  computed,
  Signal,
  signal,
  WritableSignal,
  ChangeDetectionStrategy,
  effect,
} from '@angular/core';
import { TradeStreamService } from '../trade-stream';
import { inject } from '@angular/core';
import { TradeRow } from '../models/trade-row.model';
import { scan, auditTime, debounceTime, switchMap, map } from 'rxjs/operators';
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { scanTradeTable } from '../trade-table.logic';
import { SYMBOLS } from '../symbols';
import { concat, Observable, of, timer } from 'rxjs';
import { TableModule } from 'primeng/table';
import { CheckboxModule } from 'primeng/checkbox';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-trade-table',
  imports: [TableModule, CheckboxModule, FormsModule],
  templateUrl: './trade-table.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrl: './trade-table.css',
})
export class TradeTable {

  constructor() {
    effect(() => {
      this.tradeStreamService.updateSubscription(this.debouncedCheckedSymbols());
    });
  }

  availableSymbols: string[] = SYMBOLS;
  checkedSymbols: WritableSignal<string[]> = signal<string[]>([...this.availableSymbols]);
  private tradeStreamService: TradeStreamService = inject(TradeStreamService);

  private debouncedCheckedSymbols = toSignal(
    toObservable(this.checkedSymbols).pipe(debounceTime(500)),
    { initialValue: this.checkedSymbols() }
  )

  private table$: Observable<Record<string, TradeRow>> = this.tradeStreamService.trade$.pipe(
    scan(scanTradeTable, {} as Record<string, TradeRow>),
    auditTime(500),
  );

  private tradeTableSignal = toSignal(this.table$, {
    initialValue: {} as Record<string, TradeRow>,
  });

  tradeTableSignalArray: Signal<TradeRow[]> = computed<TradeRow[]>(() =>
    Object.values(this.tradeTableSignal()).filter((row) => this.debouncedCheckedSymbols().includes(row.symbol)),
  );

  rateLimitMessage = toSignal(
    this.tradeStreamService.rateLimitNotification$.pipe(
      switchMap(notice => concat(
        of(notice),
        timer(3000).pipe(map(() => null))
      ))
    ), 
    {
      initialValue: null
    })

  onCheckBoxChange(symbol: string, event: Event) {
    const isChecked = (event.target as HTMLInputElement).checked;

    this.checkedSymbols.update((current) => {
      if (isChecked) {
        return current.includes(symbol) ? current : [...current, symbol]
      } else {
        return current.filter((s) => s !== symbol);
      }
    });
  }
}

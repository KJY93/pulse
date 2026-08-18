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
import { scan, auditTime } from 'rxjs/operators';
import { toSignal } from '@angular/core/rxjs-interop';
import { scanTradeTable } from '../trade-table.logic';
import { SYMBOLS } from '../symbols';
import { Observable } from 'rxjs';
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
      this.tradeStreamService.updateSubscription(this.checkedSymbols());
    });
  }

  availableSymbols: string[] = SYMBOLS;
  checkedSymbols: WritableSignal<string[]> = signal<string[]>([...this.availableSymbols]);
  private tradeStreamService: TradeStreamService = inject(TradeStreamService);


  private table$: Observable<Record<string, TradeRow>> = this.tradeStreamService.trade$.pipe(
    scan(scanTradeTable, {} as Record<string, TradeRow>),
    auditTime(500),
  );

  private tradeTableSignal = toSignal(this.table$, {
    initialValue: {} as Record<string, TradeRow>,
  });

  tradeTableSignalArray: Signal<TradeRow[]> = computed<TradeRow[]>(() =>
    Object.values(this.tradeTableSignal()).filter((row) => this.checkedSymbols().includes(row.symbol)),
  );

  onCheckBoxChange(symbol: string, event: Event) {
    const isChecked = (event.target as HTMLInputElement).checked;

    this.checkedSymbols.update((current) => {
      if (isChecked) {
        return current.includes(symbol) ? current : [...current, symbol]
      } else {
        return current.filter((s) => s !== symbol);
      }
    });

    this.tradeStreamService.updateSubscription(this.checkedSymbols());
  }
}

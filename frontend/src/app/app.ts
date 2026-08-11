import { Component, signal, ChangeDetectionStrategy } from '@angular/core';
import { TradeTable } from './trade-table/trade-table';

@Component({
  selector: 'app-root',
  imports: [TradeTable],
  templateUrl: './app.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrl: './app.css',
})
export class App {
  protected readonly title = signal('frontend');
}

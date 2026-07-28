import { Component, signal } from '@angular/core';
import { TradeTable } from './trade-table/trade-table';

@Component({
  selector: 'app-root',
  imports: [TradeTable],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}

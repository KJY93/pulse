import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TradeTable } from './trade-table';
import { TradeStreamService } from '../trade-stream';
import { Subject } from 'rxjs';
import { Trade } from '../models/trade.model';

describe('TradeTable', () => {
  let component: TradeTable;
  let fixture: ComponentFixture<TradeTable>;
  let fakeTradeSubject: Subject<Trade>;

  beforeEach(async () => {
    fakeTradeSubject = new Subject();
    vi.useFakeTimers();

    await TestBed.configureTestingModule({
      imports: [TradeTable],
      providers: [ { provide: TradeStreamService, useValue: { trade$: fakeTradeSubject, updateSubscription: () => {} } } ]
    }).compileComponents();

    fixture = TestBed.createComponent(TradeTable);
    component = fixture.componentInstance;

    await vi.runAllTimersAsync();    
    await fixture.whenStable();
  });

  afterEach(() => {
    vi.useRealTimers();                         
  });  

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should push a fake trade', async () => {
    fakeTradeSubject.next({
      symbol: "BTCUSDT",
      price: 67123.99,
      quantity: 0.5312
    });

    await vi.advanceTimersByTimeAsync(500);
    const tradeTable = component.tradeTableSignalArray();
    expect(tradeTable).toEqual([
      {
        symbol: "BTCUSDT",
        currentPrice: 67123.99,
        prevPrice: 67123.99,
        delta: 0,
        quantity: 0.5312
      }
    ])
  })
});
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TradeTable } from './trade-table';

describe('TradeTable', () => {
  let component: TradeTable;
  let fixture: ComponentFixture<TradeTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TradeTable],
    }).compileComponents();

    fixture = TestBed.createComponent(TradeTable);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

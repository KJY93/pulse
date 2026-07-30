import { TestBed } from '@angular/core/testing';

import { TradeStreamService } from './trade-stream';

describe('TradeStream', () => {
  let service: TradeStreamService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TradeStreamService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

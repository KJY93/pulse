import { TestBed } from '@angular/core/testing';

import { TradeStream } from './trade-stream';

describe('TradeStream', () => {
  let service: TradeStream;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TradeStream);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

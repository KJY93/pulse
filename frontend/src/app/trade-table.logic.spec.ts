import { scanTradeTable } from "./trade-table.logic";
import { test, expect } from 'vitest';

test('adds the first trade for a new symbol', () => {
    const result = scanTradeTable({}, { symbol: "BTCUSDT", price: 67432.10, quantity: 0.0012 });
    expect(result).toEqual({
        BTCUSDT: {
            symbol: "BTCUSDT",
            currentPrice: 67432.10,
            prevPrice: 67432.10,
            delta: 0,
            quantity: 0.0012
        }
    })
})

test('correctly updates prevPrice on a second trade for the same symbol', () => {
    const afterFirst = scanTradeTable({}, { symbol: "BTCUSDT", price: 67432.10, quantity: 0.0012 });
    const afterSecond = scanTradeTable(afterFirst, { symbol: "BTCUSDT", price: 67440.00, quantity: 0.0025 });

    expect(afterSecond['BTCUSDT'].prevPrice).toBe(67432.10);
    expect(afterSecond['BTCUSDT'].currentPrice).toBe(67440.00);
});
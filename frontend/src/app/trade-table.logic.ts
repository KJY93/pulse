import { TradeRow } from "./models/trade-row.model";
import { Trade } from "./models/trade.model";

export function scanTradeTable(acc: Record<string, TradeRow>, curr: Trade): Record<string, TradeRow> {
    const existing = acc[curr.symbol];
    const prevPrice = existing ? existing.currentPrice : curr.price;
    const newRow: TradeRow = {
    symbol: curr.symbol,
    currentPrice: curr.price,
    prevPrice: prevPrice,
    delta: curr.price - prevPrice,
    quantity: curr.quantity,
    };
    return { ...acc, [curr.symbol]: newRow };
}
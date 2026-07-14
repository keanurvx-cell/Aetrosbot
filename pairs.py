# pairs.py — All Pocket Option pairs from screenshots
# Format: { "SYMBOL": { "name": "Display Name", "flag": "emoji", "payout": 92 } }

FOREX_OTC = {
    "EUR/USD OTC":  {"name": "EUR/USD OTC",  "flag": "🇪🇺🇺🇸", "payout": 92},
    "GBP/USD OTC":  {"name": "GBP/USD OTC",  "flag": "🇬🇧🇺🇸", "payout": 92},
    "AUD/USD OTC":  {"name": "AUD/USD OTC",  "flag": "🇦🇺🇺🇸", "payout": 92},
    "NZD/USD OTC":  {"name": "NZD/USD OTC",  "flag": "🇳🇿🇺🇸", "payout": 92},
    "USD/CAD OTC":  {"name": "USD/CAD OTC",  "flag": "🇺🇸🇨🇦", "payout": 92},
    "AUD/CAD OTC":  {"name": "AUD/CAD OTC",  "flag": "🇦🇺🇨🇦", "payout": 92},
    "AUD/CHF OTC":  {"name": "AUD/CHF OTC",  "flag": "🇦🇺🇨🇭", "payout": 92},
    "AUD/NZD OTC":  {"name": "AUD/NZD OTC",  "flag": "🇦🇺🇳🇿", "payout": 92},
    "CAD/JPY OTC":  {"name": "CAD/JPY OTC",  "flag": "🇨🇦🇯🇵", "payout": 92},
    "EUR/NZD OTC":  {"name": "EUR/NZD OTC",  "flag": "🇪🇺🇳🇿", "payout": 92},
    "GBP/JPY OTC":  {"name": "GBP/JPY OTC",  "flag": "🇬🇧🇯🇵", "payout": 92},
    "MAD/USD OTC":  {"name": "MAD/USD OTC",  "flag": "🇲🇦🇺🇸", "payout": 92},
    "NZD/JPY OTC":  {"name": "NZD/JPY OTC",  "flag": "🇳🇿🇯🇵", "payout": 92},
    "UAH/USD OTC":  {"name": "UAH/USD OTC",  "flag": "🇺🇦🇺🇸", "payout": 92},
    "USD/BRL OTC":  {"name": "USD/BRL OTC",  "flag": "🇺🇸🇧🇷", "payout": 92},
    "USD/CNH OTC":  {"name": "USD/CNH OTC",  "flag": "🇺🇸🇨🇳", "payout": 92},
    "USD/EGP OTC":  {"name": "USD/EGP OTC",  "flag": "🇺🇸🇪🇬", "payout": 92},
    "USD/PHP OTC":  {"name": "USD/PHP OTC",  "flag": "🇺🇸🇵🇭", "payout": 92},
    "USD/SGD OTC":  {"name": "USD/SGD OTC",  "flag": "🇺🇸🇸🇬", "payout": 92},
    "USD/THB OTC":  {"name": "USD/THB OTC",  "flag": "🇺🇸🇹🇭", "payout": 92},
    "YER/USD OTC":  {"name": "YER/USD OTC",  "flag": "🇾🇪🇺🇸", "payout": 92},
    "BHD/CNY OTC":  {"name": "BHD/CNY OTC",  "flag": "🇧🇭🇨🇳", "payout": 91},
    "USD/CHF OTC":  {"name": "USD/CHF OTC",  "flag": "🇺🇸🇨🇭", "payout": 91},
    "EUR/GBP OTC":  {"name": "EUR/GBP OTC",  "flag": "🇪🇺🇬🇧", "payout": 87},
    "EUR/RUB OTC":  {"name": "EUR/RUB OTC",  "flag": "🇪🇺🇷🇺", "payout": 87},
    "USD/RUB OTC":  {"name": "USD/RUB OTC",  "flag": "🇺🇸🇷🇺", "payout": 87},
    "QAR/CNY OTC":  {"name": "QAR/CNY OTC",  "flag": "🇶🇦🇨🇳", "payout": 86},
    "USD/IDR OTC":  {"name": "USD/IDR OTC",  "flag": "🇺🇸🇮🇩", "payout": 86},
    "CHF/JPY OTC":  {"name": "CHF/JPY OTC",  "flag": "🇨🇭🇯🇵", "payout": 85},
    "EUR/TRY OTC":  {"name": "EUR/TRY OTC",  "flag": "🇪🇺🇹🇷", "payout": 82},
    "EUR/CHF OTC":  {"name": "EUR/CHF OTC",  "flag": "🇪🇺🇨🇭", "payout": 80},
    "AUD/JPY OTC":  {"name": "AUD/JPY OTC",  "flag": "🇦🇺🇯🇵", "payout": 78},
    "USD/ARS OTC":  {"name": "USD/ARS OTC",  "flag": "🇺🇸🇦🇷", "payout": 78},
    "ZAR/USD OTC":  {"name": "ZAR/USD OTC",  "flag": "🇿🇦🇺🇸", "payout": 78},
    "GBP/AUD OTC":  {"name": "GBP/AUD OTC",  "flag": "🇬🇧🇦🇺", "payout": 48},
    "CAD/CHF OTC":  {"name": "CAD/CHF OTC",  "flag": "🇨🇦🇨🇭", "payout": 48},
    "SAR/CNY OTC":  {"name": "SAR/CNY OTC",  "flag": "🇸🇦🇨🇳", "payout": 47},
    "JOD/CNY OTC":  {"name": "JOD/CNY OTC",  "flag": "🇯🇴🇨🇳", "payout": 46},
    "USD/CLP OTC":  {"name": "USD/CLP OTC",  "flag": "🇺🇸🇨🇱", "payout": 75},
    "KES/USD OTC":  {"name": "KES/USD OTC",  "flag": "🇰🇪🇺🇸", "payout": 73},
    "LBP/USD OTC":  {"name": "LBP/USD OTC",  "flag": "🇱🇧🇺🇸", "payout": 72},
    "USD/BDT OTC":  {"name": "USD/BDT OTC",  "flag": "🇺🇸🇧🇩", "payout": 72},
    "USD/VND OTC":  {"name": "USD/VND OTC",  "flag": "🇺🇸🇻🇳", "payout": 71},
    "USD/INR OTC":  {"name": "USD/INR OTC",  "flag": "🇺🇸🇮🇳", "payout": 69},
    "USD/MXN OTC":  {"name": "USD/MXN OTC",  "flag": "🇺🇸🇲🇽", "payout": 68},
    "EUR/JPY OTC":  {"name": "EUR/JPY OTC",  "flag": "🇪🇺🇯🇵", "payout": 67},
    "AED/CNY OTC":  {"name": "AED/CNY OTC",  "flag": "🇦🇪🇨🇳", "payout": 62},
    "USD/DZD OTC":  {"name": "USD/DZD OTC",  "flag": "🇺🇸🇩🇿", "payout": 62},
    "USD/PKR OTC":  {"name": "USD/PKR OTC",  "flag": "🇺🇸🇵🇰", "payout": 60},
    "CHF/NOK OTC":  {"name": "CHF/NOK OTC",  "flag": "🇨🇭🇳🇴", "payout": 58},
    "EUR/HUF OTC":  {"name": "EUR/HUF OTC",  "flag": "🇪🇺🇭🇺", "payout": 58},
    "NZD/USD OTC":  {"name": "NZD/USD OTC",  "flag": "🇳🇿🇺🇸", "payout": 58},
    "NGN/USD OTC":  {"name": "NGN/USD OTC",  "flag": "🇳🇬🇺🇸", "payout": 55},
    "TND/USD OTC":  {"name": "TND/USD OTC",  "flag": "🇹🇳🇺🇸", "payout": 55},
    "OMR/CNY OTC":  {"name": "OMR/CNY OTC",  "flag": "🇴🇲🇨🇳", "payout": 54},
    "USD/COP OTC":  {"name": "USD/COP OTC",  "flag": "🇺🇸🇨🇴", "payout": 41},
    "USD/JPY OTC":  {"name": "USD/JPY OTC",  "flag": "🇺🇸🇯🇵", "payout": 40},
    "USD/MYR OTC":  {"name": "USD/MYR OTC",  "flag": "🇺🇸🇲🇾", "payout": 28},
}

CRYPTO_OTC = {
    "Dogecoin OTC":     {"name": "Dogecoin OTC",     "flag": "🐶", "payout": 92},
    "Ethereum OTC":     {"name": "Ethereum OTC",     "flag": "🔷", "payout": 92},
    "Toncoin OTC":      {"name": "Toncoin OTC",      "flag": "💎", "payout": 92},
    "Bitcoin ETF OTC":  {"name": "Bitcoin ETF OTC",  "flag": "🟡", "payout": 84},
    "Chainlink OTC":    {"name": "Chainlink OTC",    "flag": "🔗", "payout": 83},
    "TRON OTC":         {"name": "TRON OTC",         "flag": "🔴", "payout": 83},
    "Avalanche OTC":    {"name": "Avalanche OTC",    "flag": "🔺", "payout": 75},
    "Polkadot OTC":     {"name": "Polkadot OTC",     "flag": "⚫", "payout": 64},
    "Solana OTC":       {"name": "Solana OTC",       "flag": "🟣", "payout": 64},
    "Bitcoin OTC":      {"name": "Bitcoin OTC",      "flag": "🟡", "payout": 61},
    "BNB OTC":          {"name": "BNB OTC",          "flag": "🟨", "payout": 58},
    "Litecoin OTC":     {"name": "Litecoin OTC",     "flag": "⚪", "payout": 57},
    "Cardano OTC":      {"name": "Cardano OTC",      "flag": "💙", "payout": 48},
    "Polygon OTC":      {"name": "Polygon OTC",      "flag": "🟪", "payout": 28},
}

STOCKS_OTC = {
    "Apple OTC":              {"name": "Apple OTC",              "flag": "🍎",  "payout": 92},
    "Boeing OTC":             {"name": "Boeing OTC",             "flag": "✈️",  "payout": 92},
    "Facebook OTC":           {"name": "Facebook / Meta OTC",    "flag": "📘",  "payout": 92},
    "Johnson & Johnson OTC":  {"name": "Johnson & Johnson OTC",  "flag": "💊",  "payout": 92},
    "McDonald's OTC":         {"name": "McDonald's OTC",         "flag": "🍔",  "payout": 92},
    "Pfizer OTC":             {"name": "Pfizer Inc OTC",         "flag": "💉",  "payout": 92},
    "Amazon OTC":             {"name": "Amazon OTC",             "flag": "📦",  "payout": 92},
    "Citigroup OTC":          {"name": "Citigroup Inc OTC",      "flag": "🏦",  "payout": 92},
    "FedEx OTC":              {"name": "FedEx OTC",              "flag": "🚚",  "payout": 92},
    "GameStop OTC":           {"name": "GameStop Corp OTC",      "flag": "🎮",  "payout": 89},
    "Coinbase OTC":           {"name": "Coinbase Global OTC",    "flag": "🪙",  "payout": 85},
    "VISA OTC":               {"name": "VISA OTC",               "flag": "💳",  "payout": 85},
    "Netflix OTC":            {"name": "Netflix OTC",            "flag": "🎬",  "payout": 84},
    "Palantir OTC":           {"name": "Palantir Technologies OTC","flag": "🔭", "payout": 84},
    "Cisco OTC":              {"name": "Cisco OTC",              "flag": "🔌",  "payout": 82},
    "VIX OTC":                {"name": "VIX OTC",                "flag": "📉",  "payout": 81},
    "Intel OTC":              {"name": "Intel OTC",              "flag": "🔲",  "payout": 77},
    "American Express OTC":   {"name": "American Express OTC",   "flag": "💳",  "payout": 75},
    "ExxonMobil OTC":         {"name": "ExxonMobil OTC",         "flag": "🛢️",  "payout": 54},
    "Microsoft OTC":          {"name": "Microsoft OTC",          "flag": "🪟",  "payout": 53},
    "Tesla OTC":              {"name": "Tesla OTC",              "flag": "⚡",  "payout": 53},
    "AMD OTC":                {"name": "Advanced Micro Devices OTC","flag": "🔴","payout": 49},
    "Alibaba OTC":            {"name": "Alibaba OTC",            "flag": "🛍️",  "payout": 43},
    "Marathon Digital OTC":   {"name": "Marathon Digital Holdings OTC","flag": "⛏️","payout": 32},
}

COMMODITIES_OTC = {
    "Brent Oil OTC":     {"name": "Brent Oil OTC",     "flag": "🛢️", "payout": 88},
    "WTI Crude Oil OTC": {"name": "WTI Crude Oil OTC", "flag": "🛢️", "payout": 88},
    "Silver OTC":        {"name": "Silver OTC",        "flag": "🥈", "payout": 88},
    "Gold OTC":          {"name": "Gold OTC",          "flag": "🥇", "payout": 88},
    "Natural Gas OTC":   {"name": "Natural Gas OTC",   "flag": "⛽", "payout": 53},
    "Palladium OTC":     {"name": "Palladium spot OTC","flag": "🔳", "payout": 53},
    "Platinum OTC":      {"name": "Platinum spot OTC", "flag": "⬜", "payout": 53},
}

INDICES_OTC = {
    "AUS200 OTC": {"name": "AUS 200 OTC",  "flag": "🇦🇺📊", "payout": 75},
    "US100 OTC":  {"name": "US100 OTC",   "flag": "🇺🇸💻", "payout": 53},
    "SP500 OTC":  {"name": "SP500 OTC",   "flag": "🇺🇸📈", "payout": 53},
    "100GBP OTC": {"name": "100GBP OTC",  "flag": "🇬🇧📊", "payout": 53},
    "D30EUR OTC": {"name": "D30EUR OTC",  "flag": "🇩🇪📊", "payout": 53},
    "DJI30 OTC":  {"name": "DJI30 OTC",  "flag": "🇺🇸🏭", "payout": 53},
    "E35EUR OTC": {"name": "E35EUR OTC",  "flag": "🇪🇸📊", "payout": 53},
    "E50EUR OTC": {"name": "E50EUR OTC",  "flag": "🇪🇺📊", "payout": 53},
    "F40EUR OTC": {"name": "F40EUR OTC",  "flag": "🇫🇷📊", "payout": 53},
    "JPN225 OTC": {"name": "JPN225 OTC", "flag": "🇯🇵📊", "payout": 53},
}

def get_all_pairs():
    return {
        "Forex OTC":      FOREX_OTC,
        "Crypto OTC":     CRYPTO_OTC,
        "Stocks OTC":     STOCKS_OTC,
        "Commodities OTC":COMMODITIES_OTC,
        "Indices OTC":    INDICES_OTC,
    }

def get_high_payout_pairs(min_payout=75):
    """Return only pairs with payout >= min_payout."""
    result = {}
    for cat, pairs in get_all_pairs().items():
        for sym, info in pairs.items():
            if info["payout"] >= min_payout:
                result[sym] = {**info, "category": cat}
    return result
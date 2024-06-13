import yfinance as yf
from cachetools import TTLCache
import logging
import quantstats as qs
import plotly
from cachetools.func import ttl_cache
import plotly.graph_objects as go


def to_plotly(fig):
    try:
        return plotly.tools.mpl_to_plotly(fig)
    except Exception as ex:
        logging.error(f"Failed to convert to plotly: {ex}")
        return None


class _TickerData:
    # singleton cache for ticker data
    _ticker_info_cache = TTLCache(maxsize=1024, ttl=60)
    FAST_INFO = ['currency', 'dayHigh', 'dayLow', 'exchange', 'fiftyDayAverage', 'lastPrice', 'lastVolume', 'marketCap', 'open', 'previousClose', 'quoteType', 'regularMarketPreviousClose', 'shares', 'tenDayAverageVolume', 'threeMonthAverageVolume', 'timezone', 'twoHundredDayAverage', 'yearChange', 'yearHigh', 'yearLow']

    @staticmethod
    @ttl_cache(ttl=3600, maxsize=1024)
    def download_returns(symbol):
        returns = qs.utils.download_returns(symbol)
        return returns

    @staticmethod
    def get_data(symbol, method_name):
        if symbol not in _TickerData._ticker_info_cache:
            logging.info(f"Create ticker {symbol}")
            _TickerData._ticker_info_cache[symbol] = yf.Ticker(symbol)

        values = getattr(_TickerData._ticker_info_cache[symbol], method_name)
        return values

    @staticmethod
    def get_fast_info(symbol):
        info = _TickerData.get_data(symbol, "info")
        fast_info = {
            key: info.get(key, "") for key in _TickerData.FAST_INFO
        }
        return fast_info


class TickerInfo:

    @staticmethod
    def company_info(**kwargs):
        info = _TickerData.get_data(kwargs.get("symbol"), "info")
        officers = info.get("companyOfficers", [])
        fast_info = _TickerData.get_fast_info(kwargs.get("symbol"))
        fast_info.update({
            "symbol": info.get("symbol", ""),
            "exchange": info.get("exchange", ""),
            "address": info.get("address1", ""),
            "city": info.get("city", ""),
            "state": info.get("state", ""),
            "zip": info.get("zip", ""),
            "country": info.get("country", ""),
            "phone": info.get("phone", ""),
            "website": info.get("website", ""),
            "industry": info.get("industry", ""),
            "sector": info.get("sector", ""),
            "longBusinessSummary": info.get("longBusinessSummary", ""),
            "longName": info.get("longName", ""),
            "shortName": info.get("shortName", ""),
            "fullTimeEmployees": info.get("fullTimeEmployees", ""),
            # "companyOfficers": [{
            #     "name": x.get("name", ""),
            #     "title": x.get("title", ""),
            #     "yearBorn": x.get("yearBorn", ""),
            #     "fiscalYear": x.get("fiscalYear", "")
            # } for x in officers]
        })
        return fast_info, None

    @staticmethod
    def valuation_measures(**kwargs):
        info = _TickerData.get_data(kwargs.get("symbol"), "info")
        return {
            "symbol": info.get("symbol", ""),
            "marketCap": info.get("marketCap", 0),
            "enterpriseValue": info.get("enterpriseValue", 0),
            "currency": info.get("currency", ""),
            "beta": info.get("beta", 0),
            "trailingPE": info.get("trailingPE", 0),
            "forwardPE": info.get("forwardPE", 0),
            "pegRatio": info.get("pegRatio", 0),
            "priceToSalesTrailing12Months": info.get("priceToSalesTrailing12Months", 0),
            "priceToBook": info.get("priceToBook", 0),
            "enterpriseToRevenue": info.get("enterpriseToRevenue", 0),
            "enterpriseToEbitda": info.get("enterpriseToEbitda", 0)
        }, None

    @staticmethod
    def trading_information(**kwargs):
        info = _TickerData.get_data(kwargs.get("symbol"), "info")
        return {
            "symbol": kwargs.get("symbol"),
            "priceHint": info.get("priceHint", 0),
            "previousClose": info.get("previousClose", 0),
            "open": info.get("open", 0),
            "dayLow": info.get("dayLow", 0),
            "dayHigh": info.get("dayHigh", 0),
            "regularMarketPreviousClose": info.get("regularMarketPreviousClose", 0),
            "regularMarketOpen": info.get("regularMarketOpen", 0),
            "regularMarketDayLow": info.get("regularMarketDayLow", 0),
            "regularMarketDayHigh": info.get("regularMarketDayHigh", 0),
            "currency": info.get("currency", ""),
            "financialCurrency": info.get("financialCurrency", ""),
            "currentPrice": info.get("currentPrice", 0),
            "volume": info.get("volume", 0),
            "regularMarketVolume": info.get("regularMarketVolume", 0),
            "beta": info.get("beta", 0),
            "trailingPE": info.get("trailingPE", 0),
            "forwardPE": info.get("forwardPE", 0),
            "priceToBook": info.get("priceToBook", 0),
            "pegRatio": info.get("pegRatio", 0),
            "trailingPegRatio": info.get("trailingPegRatio", 0),
            "bid": info.get("bid", 0),
            "ask": info.get("ask", 0),
            "bidSize": info.get("bidSize", 0),
            "askSize": info.get("askSize", 0),
            "marketCap": info.get("marketCap", 0),
            "targetHighPrice": info.get("targetHighPrice", 0),
            "targetLowPrice": info.get("targetLowPrice", 0),
            "targetMeanPrice": info.get("targetMeanPrice", 0),
            "targetMedianPrice": info.get("targetMedianPrice", 0),
            "recommendationMean": info.get("recommendationMean", 0),
            "recommendationKey": info.get("recommendationKey", ""),
        }, None

    @staticmethod
    def dividend_data(**kwargs):
        info = _TickerData.get_data(kwargs.get("symbol"), "info")
        return {
            "symbol": kwargs.get("symbol"),
            "dividendRate": info.get("dividendRate", 0),
            "dividendYield": info.get("dividendYield", 0),
            "payoutRatio": info.get("payoutRatio", 0),
            "fiveYearAvgDividendYield": info.get("fiveYearAvgDividendYield", 0),
            "trailingAnnualDividendRate": info.get("trailingAnnualDividendRate", 0),
            "trailingAnnualDividendYield": info.get("trailingAnnualDividendYield", 0),
            "lastDividendValue": info.get("lastDividendValue", 0),
        }, None

    @staticmethod
    def financial_summary(**kwargs):
        info = _TickerData.get_data(kwargs.get("symbol"), "info")
        return {
            "symbol": kwargs.get("symbol"),
            "totalCash": info.get("totalCash", 0),
            "totalCashPerShare": info.get("totalCashPerShare", 0),
            "ebitda": info.get("ebitda", 0),
            "totalDebt": info.get("totalDebt", 0),
            "quickRatio": info.get("quickRatio", 0),
            "currentRatio": info.get("currentRatio", 0),
            "totalRevenue": info.get("totalRevenue", 0),
            "debtToEquity": info.get("debtToEquity", 0),
            "revenuePerShare": info.get("revenuePerShare", 0),
            "returnOnAssets": info.get("returnOnAssets", 0),
            "returnOnEquity": info.get("returnOnEquity", 0),
            "freeCashflow": info.get("freeCashflow", 0),
            "operatingCashflow": info.get("operatingCashflow", 0),
            "earningsQuarterlyGrowth": info.get("earningsQuarterlyGrowth", 0),
            "netIncomeToCommon": info.get("netIncomeToCommon", 0),
            "trailingEps": info.get("trailingEps", 0),
            "forwardEps": info.get("forwardEps", 0),
            "earningsGrowth": info.get("earningsGrowth", 0),
            "revenueGrowth": info.get("revenueGrowth", 0),
            "grossMargins": info.get("grossMargins", 0),
            "ebitdaMargins": info.get("ebitdaMargins", 0),
            "operatingMargins": info.get("operatingMargins", 0),
            "financialCurrency": info.get("financialCurrency", "")
        }, None

    @staticmethod
    def show_stock_performance(**kwargs):
        returns = _TickerData.download_returns(kwargs.get("symbol"))
        fig = qs.plots.snapshot(returns, show=False)
        fig.title = f'{kwargs.get("symbol")} Performance'
        return {
            "symbol": kwargs.get("symbol"),
            "data": _TickerData.get_fast_info(kwargs.get("symbol")),
        }, to_plotly(fig)

    @staticmethod
    def show_stock_cumulative_returns(**kwargs):
        returns = _TickerData.download_returns(kwargs.get("symbol"))
        fig = qs.plots.returns(returns, show=False, benchmark=None)
        fig.title = f'{kwargs.get("symbol")} Cumulative Returns'
        return {
            "symbol": kwargs.get("symbol"),
            "data": _TickerData.get_fast_info(kwargs.get("symbol")),
        }, to_plotly(fig)

    @staticmethod
    def show_stock_log_returns(**kwargs):
        returns = _TickerData.download_returns(kwargs.get("symbol"))
        fig = qs.plots.log_returns(returns, show=False, benchmark=None)
        fig.title = f'{kwargs.get("symbol")} Log Cumulative Returns'
        return {
            "symbol": kwargs.get("symbol"),
            "data": _TickerData.get_fast_info(kwargs.get("symbol")),
        }, to_plotly(fig)

    @staticmethod
    def show_stock_daily_returns(**kwargs):
        returns = _TickerData.download_returns(kwargs.get("symbol"))
        fig = qs.plots.daily_returns(returns, show=False, benchmark=None)
        fig.title = f'{kwargs.get("symbol")} Daily Returns'
        return {
            "symbol": kwargs.get("symbol"),
            "data": _TickerData.get_fast_info(kwargs.get("symbol")),
        }, to_plotly(fig)

    @staticmethod
    def show_stock_yearly_returns(**kwargs):
        returns = _TickerData.download_returns(kwargs.get("symbol"))
        fig = qs.plots.yearly_returns(returns, show=False, benchmark=None)
        fig.title = f'{kwargs.get("symbol")} EOY Returns'
        return {
            "symbol": kwargs.get("symbol"),
            "data": _TickerData.get_fast_info(kwargs.get("symbol")),
        }, to_plotly(fig)

    @staticmethod
    def show_stock_rolling_beta(**kwargs):
        returns = _TickerData.download_returns(kwargs.get("symbol"))
        fig = qs.plots.rolling_beta(returns, show=False, benchmark='SPY')
        fig.title = f'{kwargs.get("symbol")} Rolling Beta To SPY'
        return {
            "symbol": kwargs.get("symbol"),
            "data": _TickerData.get_fast_info(kwargs.get("symbol")),
        }, to_plotly(fig)

    @staticmethod
    def show_stock_rolling_sharpe(**kwargs):
        returns = _TickerData.download_returns(kwargs.get("symbol"))
        fig = qs.plots.rolling_sharpe(returns, show=False)
        fig.title = f'{kwargs.get("symbol")} Rolling Sharpe (6-Months)'
        return {
            "symbol": kwargs.get("symbol"),
            "data": _TickerData.get_fast_info(kwargs.get("symbol")),
        }, to_plotly(fig)

    @staticmethod
    def show_stock_rolling_sortino(**kwargs):
        returns = _TickerData.download_returns(kwargs.get("symbol"))
        fig = qs.plots.rolling_sortino(returns, show=False)
        fig.title = f'{kwargs.get("symbol")} Rolling Sortino (6-Months)'
        return {
            "symbol": kwargs.get("symbol"),
            "data": _TickerData.get_fast_info(kwargs.get("symbol")),
        }, to_plotly(fig)

    @staticmethod
    def show_stock_rolling_volatility(**kwargs):
        returns = _TickerData.download_returns(kwargs.get("symbol"))
        fig = qs.plots.rolling_volatility(returns, show=False)
        fig.title = f'{kwargs.get("symbol")} Rolling Volatility (6-Months)'
        return {
            "symbol": kwargs.get("symbol"),
            "data": _TickerData.get_fast_info(kwargs.get("symbol")),
        }, to_plotly(fig)

    @staticmethod
    def show_stock_monthly_return_heatmap(**kwargs):
        returns = _TickerData.download_returns(kwargs.get("symbol"))
        fig = qs.plots.monthly_heatmap(returns, show=False)
        fig.title = f'{kwargs.get("symbol")} Monthly Returns (%)'
        return {
            "symbol": kwargs.get("symbol"),
            "data": _TickerData.get_fast_info(kwargs.get("symbol")),
        }, to_plotly(fig)

    @staticmethod
    def show_ohlc_price_volume_history(**kwargs):
        symbol = kwargs.get("symbol")
        data = _TickerData.get_data(symbol, "history")(period='2y').reset_index()
        fig = go.Figure(
            data=go.Ohlc(
                x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])
        )
        title = f'{kwargs.get("symbol")} OHLC from {data.Date.min().strftime("%Y-%m-%d")} to {data.Date.max().strftime("%Y-%m-%d")}'
        fig.update_layout(
            title=title,
        )
        return {
            "symbol": kwargs.get("symbol"),
            "data": f"{data.iloc[0].__str__()}\n-----\n{data.iloc[-1].__str__()}\n-----\nInfo: {_TickerData.get_fast_info(symbol)}",
        }, fig

    #
    # @staticmethod
    # def dividends(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "dividends")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def splits(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "splits")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def income_stmt(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "income_stmt")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def quarterly_income_stmt(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "quarterly_income_stmt")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def balance_sheet(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "balance_sheet")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def quarterly_balance_sheet(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "quarterly_balance_sheet")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def cashflow(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "cashflow")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def quarterly_cashflow(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "quarterly_cashflow")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def major_holders(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "major_holders")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def institutional_holders(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "institutional_holders")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def mutualfund_holders(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "mutualfund_holders")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def insider_transactions(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "insider_transactions")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def insider_purchases(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "insider_purchases")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def insider_roster_holders(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "insider_roster_holders")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def recommendations(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "recommendations")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def recommendations_summary(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "recommendations_summary")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }
    #
    # @staticmethod
    # def upgrades_downgrades(**kwargs):
    #     data = _TickerData.get_data(kwargs.get("symbol"), "upgrades_downgrades")
    #     return {
    #         "symbol": kwargs.get("symbol"),
    #         "data": data.reset_index().to_json(orient="records", date_format="iso")
    #     }


if __name__ == "__main__":
    # Example usage:
    # Print company info
    print("Company Info:")
    print(TickerInfo.company_info(symbol='MSFT'))

    print(TickerInfo.company_info(symbol='MSFT'))
    #
    # # Print risk metrics
    # print("\nRisk Metrics:")
    # print(company.risk_metrics(symbol='MSFT'))
    #
    # # Print date metrics
    # print("\nDate Metrics:")
    # print(company.date_metrics(symbol='MSFT'))
    #
    # # Print price data
    # print("\nPrice Data:")
    # print(company.price_data(symbol='MSFT'))
    #
    # # Print dividend data
    # print("\nDividend Data:")
    # print(company.dividend_data(symbol='MSFT'))
    #
    # # Print volume data
    # print("\nVolume Data:")
    # print(company.volume_data(symbol='MSFT'))
    #
    # # Print market data
    # print("\nMarket Data:")
    # print(company.market_data(symbol='MSFT'))
    #
    # # Print shares data
    # print("\nShares Data:")
    # print(company.shares_data(symbol='MSFT'))
    #
    # # Print valuation ratios
    # print("\nValuation Ratios:")
    # print(company.valuation_ratios(symbol='MSFT'))
    #
    # # Print financial data
    # print("\nFinancial Data:")
    # print(company.financial_data(symbol='MSFT'))
    #
    # # Print historical data for a specific period
    # print("\nHistorical Data (1 month):")
    # print(company.history(symbol='MSFT', period='1mo'))
    #
    # # Print dividends
    # print("\nDividends:")
    # print(company.dividends(symbol='MSFT'))
    #
    # # Print splits
    # print("\nSplits:")
    # print(company.splits(symbol='MSFT'))
    #
    # # Print quarterly income statement
    # print("\nQuarterly Income Statement:")
    # print(company.quarterly_income_stmt(symbol='MSFT'))
    #
    # # Print quarterly balance sheet
    # print("\nQuarterly Balance Sheet:")
    # print(company.quarterly_balance_sheet(symbol='MSFT'))
    #
    # # Print quarterly cash flow
    # print("\nQuarterly Cash Flow:")
    # print(company.quarterly_cashflow(symbol='MSFT'))
    #
    # # Print major holders
    # print("\nMajor Holders:")
    # print(company.major_holders(symbol='MSFT'))
    #
    # # Print institutional holders
    # print("\nInstitutional Holders:")
    # print(company.institutional_holders(symbol='MSFT'))
    #
    # # Print mutual fund holders
    # print("\nMutual Fund Holders:")
    # print(company.mutualfund_holders(symbol='MSFT'))
    #
    # # Print insider transactions
    # print("\nInsider Transactions:")
    # print(company.insider_transactions(symbol='MSFT'))
    #
    # # Print insider purchases
    # print("\nInsider Purchases:")
    # print(company.insider_purchases(symbol='MSFT'))
    #
    # # Print insider roster holders
    # print("\nInsider Roster Holders:")
    # print(company.insider_roster_holders(symbol='MSFT'))
    #
    # # Print recommendations
    # print("\nRecommendations:")
    # print(company.recommendations(symbol='MSFT'))
    #
    # # Print recommendations summary
    # print("\nRecommendations Summary:")
    # print(company.recommendations_summary(symbol='MSFT'))
    #
    # # Print upgrades/downgrades
    # print("\nUpgrades/Downgrades:")
    # print(company.upgrades_downgrades(symbol='MSFT'))

# Stratagems

"Thirty-Six Stratagems", an ancient collection of tactics and strategies used in Chinese warfare and everyday life.

This web service is intended to expose random stratagem for arbitrary time period (each GET within this period returns the same response)

To implement this, asyncio task for periodic update of current stratagem is started along with aoihttp web server flow, within single application.
Also, jinja2 is used to render final web page.
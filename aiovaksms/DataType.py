class Actions:
    @property
    async def getNumbersStatus(self):
        return "getNumbersStatus"

    @property
    async def getBalance(self):
        return "getBalance"

    @property
    async def getNumber(self):
        return "getNumber"

    @property
    async def setStatus(self):
        return "setStatus"

    @property
    async def getStatus(self):
        return "getStatus"

    @property
    async def getPrices(self):
        return "getPrices"


class Status:
    @property
    async def cancel(self):
        return "-1"

    @property
    async def ready(self):
        return "1"

    @property
    async def repeat(self):
        return "3"

    @property
    async def complete(self):
        return "6"

    @property
    async def used(self):
        return "8"

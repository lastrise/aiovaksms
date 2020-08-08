import asyncio
import aiohttp
from aiovaksms.DataType import Actions, Status


class VakSms:
    def __init__(self, key):
        self._key = key
        self._url = "https://smshub.org/stubs/handler_api.php?"

    async def request(self, action, **kwargs):
        """
        Actions:
        1) getNumberStatus
           $country? - by default is 0 (Russia)
           $operator? - [mts, tele2, megafon, beeline, any]. By default is any
           Answer: {"vk_0":57,"ok_0":59,"wa_0":240,"vi_0":3,"tg_0":79,"wb_0":119,"go_0":193,"av_0":24,"av_1":237,"fb_0":107}
        2) getBalance
           Answer: ACCESS_BALANCE:$balance (где $balance - баланс на счету)
           Errors: BAD_KEY - Неверный API-ключ
        3) getNumber
           $service
           $operator? - [mts, tele2, megafon, beeline, any]. By default is any
           $country? - by default is 0 (Russia)
           Answer: NO_NUMBERS - нет номеров
                   NO_BALANCE - закончился баланс
                   ACCESS_NUMBER:$id:$number - номер выдан ($id - id операции,$number - номер телефона)
           Errors: BAD_ACTION - некорректное действие
                   BAD_SERVICE - некорректное наименование сервиса
                   BAD_KEY - Неверный API-ключ
        4) setStatus
           $id
           $status
           Answers: ACCESS_READY - готовность номера подтверждена
                    ACCESS_RETRY_GET - ожидание нового смс
                    ACCESS_ACTIVATION - сервис успешно активирован
                    ACCESS_CANCEL - активация отменена
           Errors: ERROR_SQL - ошибка SQL-сервера
                   NO_ACTIVATION - id активации не существует
                   BAD_SERVICE - некорректное наименование сервиса
                   BAD_STATUS - некорректный статус
                   BAD_KEY - Неверный API-ключ
                   BAD_ACTION - некорректное действие
        5) getStatus
           $id
           Answers: STATUS_WAIT_CODE - ожидание смс
                    STATUS_WAIT_RETRY:$lastcode - ожидание уточнения кода (где $lastcode - прошлый, неподошедший код)
                    STATUS_WAIT_RESEND - ожидание повторной отправки смс
                    STATUS_CANCEL - активация отменена
                    STATUS_OK:$code - код получен (где $code - код активации)
           Errors: NO_ACTIVATION - id активации не существует
                   BAD_KEY - Неверный API-ключ
                   BAD_ACTION - некорректное действие
        6) getPrices
           $service?
           $country?
           Answers: {"0":{"vk":{"cost":15,"count":1307},"ok":{"cost":4,"count":2789}}}"""

        params = "api_key={}&".format(self._key) + "action={}&".format(action) +\
                 "&".join(["{}={}".format(key, kwargs[key]) for key in kwargs])

        link = self._url + params

        async with aiohttp.ClientSession() as session:
            response = await session.get(link)

            if response.status != 200:
                raise Exception("Bad status code of response!")

            errors = ["BAD_KEY", "BAD_ACTION", "BAD_SERVICE", "ERROR_SQL", "NO_ACTIVATION", "BAD_STATUS"
                                                                                            "NO_NUMBERS", "NO_BALANCE"]

            content = await response.text()

            if content in errors:
                raise Exception(content)

            if action == await Actions().getNumber:
                _id, phoneNumber = content.split(":")[1:]
                return Activation(_id, phoneNumber, self)
            elif action == await Actions().getNumbersStatus or action == await Actions().getPrices:
                return await response.json()
            elif action == await Actions().getBalance:
                return float(content.split(":")[1])

        return content


class Activation:
    def __init__(self, _id, phoneNumber, wrapper: VakSms):
        self.id = _id
        self.phoneNumber = phoneNumber
        self._wrapper = wrapper

    async def waitCode(self, timeout=60, interval=5, not_end=False):
        for i in range(0, timeout, interval):
            await asyncio.sleep(interval)
            result = await self._wrapper.request(action=await Actions().getStatus, id=self.id)
            if not result.startswith("STATUS_OK"):
                continue
            code = result.split(":")[1]
            if not_end:
                await self.repeat()
            else:
                await self.complete()

            return code

        await self.cancel()
        raise Exception("SMS-code timed out")

    async def setStatus(self, status):
        result = await self._wrapper.request(action=await Actions().setStatus, id=self.id, status=status)
        return result

    async def cancel(self):
        return await self.setStatus(await Status().cancel)

    async def complete(self):
        return await self.setStatus(await Status().complete)

    async def repeat(self):
        return await self.setStatus(await Status().repeat)

    async def ready(self):
        return await self.setStatus(await Status().ready)

    async def used(self):
        return await self.setStatus(await Status().used)

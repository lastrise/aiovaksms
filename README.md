### aiovaksms
Async wrapper for automatic reception of SMS-messages by vak-sms.com

### Installing:
```
pip3 install git+https://github.com/lastrise/aiovaksms
```

### Example:
```
async def main():
    wrapper = VakSms("fb52a93e8d8f4479856fa696998ed927")
    activation = await wrapper.request(action=await Actions().getNumber, service=await Services().Vkontakte)
    await activation.waitCode(timeout=300)


async def start():
    await asyncio.gather(main(), main())

loop = asyncio.new_event_loop()
loop.run_until_complete(start())
```

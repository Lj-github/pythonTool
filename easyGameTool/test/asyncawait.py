# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 上午10:40

async def async_function():
    return 1


async def await_coroutine():
    result = await async_function()
    print(result)


# coroutine 协程
def run(coroutine):
    try:
        coroutine.send(None)
    except StopIteration as e:
        return e.value


run(await_coroutine())

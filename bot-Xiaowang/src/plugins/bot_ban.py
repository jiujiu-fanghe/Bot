from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Event,Bot,GroupMessageEvent,GROUP_ADMIN,GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot import on_keyword,on_command
from nonebot.adapters.onebot.v11 import Message
import random


# 权限 bot超管，群管理，群主

catch_str = on_keyword({'随机禁言'},permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN)

@catch_str.handle()
async def send_msg(bot: Bot, event: GroupMessageEvent,state: T_State):
    id = event.get_user_id()
    get_msg = str(event.get_message())
    content = get_msg[5:]
    #最大禁言时间
    max_ban_time = 60
    if len(content) > 1:
        max_ban_time = random.randint(1, int(content))

    #获取群号 event.group_id
    member_list = await bot.get_group_member_list(group_id=event.group_id)

    random_num = random.randint(0, len(member_list) - 1)

    user_id = member_list[random_num]['user_id']
    nickname = member_list[random_num]['card'] or member_list[random_num]['nickname']

    try:
        await bot.set_group_ban(group_id=event.group_id, user_id=user_id,duration=60 * max_ban_time)
    except:
        msg = '[CQ:at,qq={}]'.format(id) + '\n权限不足，禁言失败'
        await catch_str.finish(Message(f'{msg}'))
        return

    msg = '[CQ:at,qq={}]'.format(id)+ '\n恭喜倒霉蛋：' + nickname + '喜提' + str(max_ban_time) + '分钟的禁言礼包'
    await catch_str.finish(Message(f"{msg}"))

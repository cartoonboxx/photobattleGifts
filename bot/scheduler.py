import asyncio
from datetime import datetime
from aiogram import Bot

from bot.utils import return_end_time_string_with_time
from bot.models import get_all_prizes, set_marker_to_prize
from bot.grammatics import decline_participant


async def contest_watcher(bot: Bot, session_maker):
    while True:
        try:
            async with session_maker() as session:
                contests = await get_all_prizes(session)
                now = datetime.now()

                for contest in contests:
                    end_time = return_end_time_string_with_time(contest.created, contest.duration_minutes)

                    if end_time <= now and not contest.isFinished:
                        try:
                            await bot.edit_message_caption(
                                chat_id=contest.channel_link,
                                caption=f"🎁 Розыгрыш {contest.prize_size}⭐️ завершён.\n\n"
                                        f"🦋 Бот определил {contest.winners_count} {decline_participant('победител', contest.winners_count)} "
                                        f"розыгрыша среди {1000} {decline_participant('участник', 1000)} и отправил "
                                        f"каждому {contest.prize_size // contest.winners_count}⭐\n\nПоздравляем победителей! 🎉",
                                message_id=contest.telegram_post_id
                            )
                            print(contest.channel_link, contest.telegram_post_id)
                            await set_marker_to_prize(session, contest.id)


                        except Exception as e:
                            print(f"[ERROR] Ошибка при отправке сообщения: {e}")


        except Exception as e:
            print(f"[ERROR] contest_watcher: {e}")

        await asyncio.sleep(1)
from apps.vk_api import VKApi

from apps.vk_bot.models import VKBotConfigModel
from apps.testing.handlers import start_testing_handler, continue_test_handler

from apps.testing.utils import delete_tag_from_text


def init_bot_api():
    if VKBotConfigModel.objects.exists():
        bot_config = VKBotConfigModel.objects.first()
        vk_api = VKApi(
            bot_token=bot_config.vk_api_key,
            group_id=bot_config.vk_group_id,
            v_api=bot_config.vk_api_v,
        )
        return vk_api, bot_config
    else:
        return None, None


vk_bot_api, bot_conf = init_bot_api()


def start_listen():
    if vk_bot_api:
        print(f"Starting Bot for - {bot_conf}")
        for event in vk_bot_api.start_polling():
            if event:
                if (event.type == "wall_reply_new") and (not event.object["from_id"] == event.object["owner_id"]):
                    text_with_out_tag = delete_tag_from_text(
                        text=event.object["text"],
                        tag=f"[club{event.group_id}|testMultibot], "
                    )
                    if text_with_out_tag.lower() == bot_conf.comment_interaction_phrase.lower():
                        if bot_conf.interaction_post == 0:
                            start_testing_handler(
                                vk_api=vk_bot_api,
                                user_id=event.object["from_id"],
                                event=event
                            )
                        elif event.object["post_id"] == bot_conf.interaction_post:
                            start_testing_handler(
                                vk_api=vk_bot_api,
                                user_id=event.object["from_id"],
                                event=event
                            )
                    else:
                        continue_test_handler(
                            vk_api=vk_bot_api,
                            user_id=event.object["from_id"],
                            event=event
                        )
    else:
        print("There no completed Bot configuration in Database. You need to configure Bot in Django Admin first")

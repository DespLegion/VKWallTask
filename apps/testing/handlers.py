from apps.bot_user.models import BotUser
from .models import TestingsModel
from .utils import create_new_test, get_testing_result, delete_tag_from_text


def continue_test_handler(vk_api, user_id, event):
    db_user = BotUser.objects.get(user_id=user_id)
    if db_user.user_q_status == "1":

        vk_user_resp = vk_api.get_user(user_id=user_id)
        vk_user = vk_user_resp["response"][0]

        reply_user_tag = f"[id{vk_user['id']}|{vk_user['first_name']}]"

        question_number = db_user.user_q_state

        user_answer = delete_tag_from_text(text=event.object["text"], tag=f"[club{event.group_id}|testMultibot], ")

        db_user_testing = TestingsModel.objects.get(user=db_user)

        user_answers_from_db = db_user_testing.testing_user_answers
        if user_answers_from_db:
            user_answers_from_db[question_number] = user_answer
            db_user_testing.testing_user_answers = user_answers_from_db
        else:
            new_user_answers = {question_number: user_answer}
            db_user_testing.testing_user_answers = new_user_answers
        db_user_testing.save()

        if int(question_number) + 1 > len(db_user_testing.testing_json):
            testing_result = get_testing_result(user_id=user_id)

            db_user.user_q_status = "2"
            db_user.user_q_state = "done"
            db_user_testing.testing_status = True
            db_user_testing.testing_res = testing_result
            db_user_testing.save()

            message = (f"{reply_user_tag}, Ваш ответ '{user_answer}'!\n\n"
                       f"Поздравляю, Вы ответили на все ({len(db_user_testing.testing_json)}) вопросы!\n"
                       f"Ваш результат: {testing_result} из 100 баллов")
        else:
            db_user.user_q_state = str(int(question_number) + 1)

            message = (f"{reply_user_tag}, Ваш ответ '{user_answer}'!\n\n"
                       f"Вопрос номер {int(question_number) + 1} из {len(db_user_testing.testing_json)}:\n"
                       f"{db_user_testing.testing_json[str(int(question_number) + 1)]['question_text']}")

        db_user.save()

        vk_api.wall_comment_answer(post_id=event.object["post_id"], message=message, reply_id=event.object["id"])


def start_testing_handler(vk_api, user_id, event):
    vk_user_resp = vk_api.get_user(user_id=user_id)
    vk_user = vk_user_resp["response"][0]

    if (not BotUser.objects.exists()) or (not BotUser.objects.filter(user_id=user_id).exists()):

        new_user = BotUser()
        new_user.user_id = vk_user["id"]
        new_user.user_firstname = vk_user["first_name"]
        new_user.user_q_status = "0"
        new_user.user_q_state = "0"

        if ("last_name" in vk_user) and (vk_user["last_name"]):
            new_user.user_lastname = vk_user["last_name"]

        new_user.save()

    reply_user_tag = f"[id{vk_user['id']}|{vk_user['first_name']}]"

    db_user = BotUser.objects.get(user_id=user_id)
    if db_user.user_q_status == "0":
        new_json_test = create_new_test()

        new_test = TestingsModel()
        new_test.user = db_user
        new_test.testing_json = new_json_test

        new_test.save()

        db_user.user_q_status = "1"
        db_user.user_q_state = "1"
        db_user.save()

        message = f"{reply_user_tag}, Вы начали новый опрос!\n\nПервый вопрос:\n{new_json_test[1]['question_text']}"
        vk_api.wall_comment_answer(post_id=event.object["post_id"], message=message, reply_id=event.object["id"])
    elif db_user.user_q_status == "1":

        db_user_testing = TestingsModel.objects.get(user=db_user)

        question_number = db_user.user_q_state

        message = (f"{reply_user_tag}, Продолжаем Ваш опрос:\n\n"
                   f"Вы остановились на вопросе номер {question_number} из {len(db_user_testing.testing_json)}:\n"
                   f"{db_user_testing.testing_json[str(question_number)]['question_text']}")

        vk_api.wall_comment_answer(post_id=event.object["post_id"], message=message, reply_id=event.object["id"])

    elif db_user.user_q_status == "2":
        testing_result = get_testing_result(user_id=user_id)
        message = f"{reply_user_tag}, Вы уже завершили свой опрос!\n\nВаш результат: {testing_result}"
        vk_api.wall_comment_answer(post_id=event.object["post_id"], message=message, reply_id=event.object["id"])

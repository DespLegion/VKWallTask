from apps.testing.models import QuestionsModel, TestingsConfig, TestingsModel


def create_new_test():
    all_questions = QuestionsModel.objects.order_by("?")
    testings_config = TestingsConfig.objects.first()
    questions_dict = {}
    counter = 0
    for question in all_questions:
        questions_dict[counter+1] = {
            "question_db_id": question.pk,
            "question_text": question.full_question,
            "question_answer": question.question_answer,
        }
        if counter + 1 >= testings_config.question_count:
            break
        counter += 1

    return questions_dict


def get_testing_result(user_id):
    user_full_testing = TestingsModel.objects.filter(user__user_id=user_id)
    user_answers = user_full_testing[0].testing_user_answers
    user_testings = user_full_testing[0].testing_json

    balls_for_q = 100 / len(user_testings)
    user_score = 0

    for question_id, answer in user_answers.items():
        if question_id in user_testings and user_testings[question_id]["question_answer"].lower() == answer.lower():
            user_score += balls_for_q

    return int(user_score)


def delete_tag_from_text(text: str, tag: str):
    if tag in text:
        return text.replace(tag, "")
    else:
        return text

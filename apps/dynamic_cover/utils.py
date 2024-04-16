from djangoVKWall import settings
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime


from .models import CoverImgsModel
from apps.testing.models import TestingsModel
from apps.vk_bot.bot_core import vk_bot_api


def upload_cover():
    image = CoverImgsModel.objects.filter(is_activ_cover=True)
    img_path = f"{settings.MEDIA_ROOT}/{image[0].cover_img}"

    b_cover = get_users_imgs(vk_bot_api, banner_img_path=img_path)

    upload_url = vk_bot_api.get_upload_cover_server()

    uploaded_photo = vk_bot_api.upload_cover(upload_url=upload_url, file_path=b_cover)

    save_status = vk_bot_api.save_uploaded_cover(hash_data=uploaded_photo["hash"], photo=uploaded_photo["photo"])

    return save_status


def get_users_imgs(vk_api, banner_img_path):
    now = datetime.now()
    cur_date = datetime.date(now)
    cur_time = datetime.time(now)
    format_cur_date = cur_date.strftime("%d.%m.%Y")
    format_cur_time = cur_time.strftime("%H:%M")

    if TestingsModel.objects.exists() and TestingsModel.objects.filter(testing_res__isnull=False).exists():

        f = TestingsModel.objects.filter(testing_res__isnull=False).order_by('-testing_res').first()
        max_score = f.testing_res
        last_top_score = TestingsModel.objects.filter(testing_res=max_score).first()

        last_top_score_vk_user = vk_api.get_user(user_id=last_top_score.user.user_id, with_photo=True)

        last_test_complete = TestingsModel.objects.filter(testing_res__isnull=False).order_by('-id').first()
        last_test_vk_user = vk_api.get_user(user_id=last_test_complete.user.user_id, with_photo=True)

        image1_path = BytesIO(vk_api.get_photo(last_top_score_vk_user["response"][0]["photo_400_orig"]))
        image2_path = BytesIO(vk_api.get_photo(last_test_vk_user["response"][0]["photo_400_orig"]))

        last_top_score_user_name = last_top_score.user.user_firstname
        last_top_score_score = last_top_score.testing_res

        last_test_complete_user_name = last_test_complete.user.user_firstname
        last_test_score = last_test_complete.testing_res
    else:
        image1_path = None
        image2_path = None

        last_top_score_user_name = None
        last_top_score_score = None

        last_test_complete_user_name = None
        last_test_score = None

    cover = create_cover_banner(
        main_image_path=banner_img_path,
        image1_path=image1_path,
        image2_path=image2_path,
        position1=(1700, 600),
        position2=(900, 600),
        name1=last_top_score_user_name,
        score1=last_top_score_score,
        name2=last_test_complete_user_name,
        score2=last_test_score,
        cur_date=format_cur_date,
        cur_time=format_cur_time,
    )

    b_cover = BytesIO()
    cover.save(b_cover, format='png')

    return b_cover


def create_cover_banner(
        main_image_path,
        position1,
        position2,
        cur_date,
        cur_time,
        name1=None,
        name2=None,
        score1=None,
        score2=None,
        image1_path=None,
        image2_path=None,
):
    main_image = Image.open(main_image_path)

    font = ImageFont.truetype('arial.ttf', 30)

    main_draw = ImageDraw.Draw(main_image)

    new_image = Image.new('RGBA', main_image.size, (255, 255, 255, 0))

    if image1_path and name1 and score1:

        image1 = Image.open(image1_path).resize((150, 150))

        mask1 = Image.new('L', image1.size, 0)
        draw1 = ImageDraw.Draw(mask1)
        draw1.ellipse((0, 0, 150, 150), fill=255)

        new_image1 = Image.new('RGBA', image1.size, (255, 255, 255, 0))
        new_image1.paste(image1, (0, 0), mask1)

        main_draw.text((position1[0] - 470, position1[1]), "Последний наивысший балл:", fill="white", font=font)
        main_draw.text((position1[0] - 470, position1[1] + 50), f"{name1}", fill="white", font=font)
        main_draw.text((position1[0] - 470, position1[1] + 100), f"{score1} баллов из 100", fill="white", font=font)

        new_image.paste(new_image1, position1)

    if image2_path and name2 and score2:

        image2 = Image.open(image2_path).resize((150, 150))

        mask2 = Image.new('L', image2.size, 0)
        draw2 = ImageDraw.Draw(mask2)
        draw2.ellipse((0, 0, 150, 150), fill=255)

        new_image2 = Image.new('RGBA', image2.size, (255, 255, 255, 0))
        new_image2.paste(image2, (0, 0), mask2)

        main_draw.text((position2[0] - 500, position2[1]), "Последний прошедший опрос:", fill="white", font=font)
        main_draw.text((position2[0] - 500, position2[1] + 50), f"{name2}", fill="white", font=font)
        main_draw.text((position2[0] - 500, position2[1] + 100), f"{score2} баллов из 100", fill="white", font=font)

        new_image.paste(new_image2, position2)

    date_font = ImageFont.load_default(size=54)
    main_draw.text((50, 150), f"{cur_date}", fill="black", font=date_font)
    main_draw.text((52, 210), f"{cur_time}", fill="black", font=date_font)

    merged_image = Image.alpha_composite(main_image.convert('RGBA'), new_image)

    return merged_image

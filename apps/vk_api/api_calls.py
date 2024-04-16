import requests as req
from .utils import fill_adict_from_dict


class VKApi:
    def __init__(self, bot_token, group_id, v_api):
        self.bot_token = bot_token
        self.group_id = group_id
        self.v_api = v_api

        self.base_url = "https://api.vk.com/method"
        self.get_poll_server_method = "groups.getLongPollServer"

        self.key = None
        self.server = None
        self.ts = None
        self.get_long_poll_server()

    def start_polling(self):
        while True:
            yield self.get_event()

    def get_event(self):
        """
        raw_event structure:
            {
                "type": "wall_post_new",
                "event_id": "c68dfb983247fea8ac98ea0ea59717df71d8064f",
                "v": "5.131",
                "object": {
                    "id": 28,
                    "from_id": -123456,
                    "owner_id": -123456,
                    "date": 1519631591,
                    "marked_as_ads": 0,
                    "post_type": "post",
                    "text": "Post text",
                    "can_edit": 1,
                    "created_by": 564321,
                    "can_delete": 1,
                    "comments": {
                        "count": 0
                    }
                },
                "group_id": 123456
            }

        :return:
        """

        updates_response = req.get(f'{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25')
        updates_data = updates_response.json()

        if 'failed' in updates_data:
            self.get_long_poll_server()
        else:
            self.ts = updates_data['ts']
            raw_event = updates_data.get('updates', [])
            print(raw_event)
            if len(raw_event) > 0:
                event = fill_adict_from_dict(raw_event[0])
                return event
            else:
                return None

    def get_long_poll_server(self):
        server_resp = req.get(
            f"{self.base_url}/{self.get_poll_server_method}"
            f"?group_id={self.group_id}&access_token={self.bot_token}&v={self.v_api}"
        )
        server_data = server_resp.json()
        self.server = server_data['response']['server']
        self.key = server_data['response']['key']
        self.ts = server_data['response']['ts']

    def get_user(self, user_id, with_photo=False):
        if with_photo:
            req_fields = f"fields=photo_400_orig"
        else:
            req_fields = ""
        server_resp = req.get(
            f"{self.base_url}/users.get?user_ids={user_id}&{req_fields}&access_token={self.bot_token}&v={self.v_api}"
        )
        json_response = server_resp.json()
        return json_response

    def wall_comment_answer(self, post_id, message, reply_id=None):
        if reply_id:
            reply_url = f"&reply_to_comment={reply_id}"
        else:
            reply_url = ""
        server_resp = req.get(
            f"{self.base_url}/wall.createComment?owner_id=-{self.group_id}&post_id={post_id}{reply_url}"
            f"&message={message}&access_token={self.bot_token}&v={self.v_api}"
        )
        json_response = server_resp.json()
        return json_response

    def get_upload_cover_server(self, crop_x=0, crop_y=0, crop_x2=1920, crop_y2=768):
        resp = req.get(f"{self.base_url}/photos.getOwnerCoverPhotoUploadServer?group_id={self.group_id}&"
                       f"crop_x={crop_x}&crop_y={crop_y}&crop_x2={crop_x2}&crop_y2={crop_y2}&"
                       f"access_token={self.bot_token}&v={self.v_api}")

        json_resp = resp.json()
        return json_resp["response"]["upload_url"]

    def upload_cover(self, upload_url, file_path):
        files = {
            'photo': file_path.getbuffer(),
        }
        resp = req.post(upload_url, files=files)
        return resp.json()

    def save_uploaded_cover(self, hash_data, photo):
        photo_data = {
            "photo": photo,
            "hash": hash_data
        }
        resp = req.post(f"{self.base_url}/photos.saveOwnerCoverPhoto?"
                        f"access_token={self.bot_token}&v={self.v_api}", params=photo_data)
        if resp.status_code == 200:
            return resp.json()
        else:
            return None

    def get_photo(self, photo_url):
        resp = req.get(photo_url)
        return resp.content

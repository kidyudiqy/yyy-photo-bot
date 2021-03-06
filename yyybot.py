#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pickle
import time
import sys
import tweepy
import config
from datetime import datetime, timezone, timedelta
from random import randint, choice
from textwrap import dedent

CARDS = []
border_files = config.illustration_path / '!Border'
bday_list = {
    (28, 2): (550020, 'Takumi', 5),
    (21, 3): (1250020, 'Komugi', 12),
    (9, 4): (150020, 'Mitsuki', 1),
    (13, 5): (1850020, 'Genshin', 18),
    (28, 5): (1050020, 'Tatsuma', 10),
    (24, 6): (950020, 'Aki', 9),
}
appearance = {
    1: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 26), (4, 15), (4, 16), (4, 37), (5, 18), (5, 19), (5, 28)],
    2: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 24), (3, 36), (4, 15), (4, 16), (4, 28), (4, 30), (5, 18), (5, 34)],
    3: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 12), (3, 28), (3, 34), (4, 15), (4, 16), (5, 18), (5, 24)],
    4: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 28), (4, 15), (4, 16), (4, 17), (4, 26), (5, 18), (5, 21)],
    5: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 23), (3, 35), (4, 15), (4, 16), (4, 28), (5, 18)],
    6: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (4, 15), (4, 16), (4, 22), (4, 32), (4, 36), (5, 18), (5, 27), (5, 38)],
    7: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 25), (3, 33), (4, 15), (4, 16), (4, 35), (4, 38), (5, 18), (5, 31)],
    8: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 27), (3, 38), (4, 15), (4, 16), (4, 26), (5, 18), (5, 35)],
    9: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 12), (3, 31), (4, 15), (4, 16), (4, 38), (5, 18), (5, 25)],
    10: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 23), (4, 15), (4, 16), (4, 17), (4, 31), (5, 18), (5, 33)],
    11: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 29), (3, 36), (4, 15), (4, 16), (4, 33), (5, 18), (5, 22)],
    12: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 22), (4, 15), (4, 16), (4, 27), (4, 33), (5, 18)],
    13: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 33), (4, 15), (4, 16), (4, 25), (4, 31), (5, 18), (5, 21)],
    14: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (4, 15), (4, 16), (4, 17), (4, 36), (5, 18), (5, 23), (5, 37)],
    15: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 30), (3, 31), (4, 15), (4, 16), (4, 23), (4, 34), (5, 18), (5, 21)],
    16: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 37), (4, 15), (4, 16), (4, 23), (5, 18), (5, 30), (5, 36)],
    17: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 26), (3, 32), (4, 15), (4, 16), (4, 24), (5, 18), (5, 29)],
    18: [(1, 1), (1, 2), (2, 4), (2, 5), (3, 9), (3, 10), (3, 11), (3, 12), (3, 38), (4, 15), (4, 16), (4, 29), (5, 18), (5, 26), (5, 32)],
}


class Card:

    _character_list = {
        1: ('Kuze Mitsuki', 'mtk', '久瀬 光希'),
        2: ('Nishikido Samon', 'smn', '錦戸 佐門'),
        3: ('Igarashi Hiro', 'hir', '五十嵐 比呂'),
        4: ('Konno Azusa', 'azs', '紺野 梓'),
        5: ('Kurumizawa Takumi', 'tkm', '胡桃沢 タクミ'),
        6: ('Fujiwara Soushi', 'sus', '藤原 蒼志'),
        7: ('Iseya Zen', 'zen', '伊勢谷 全'),
        8: ('Sanada Junnosuke', 'jns', '真田 淳之介'),
        9: ('Takachiho Aki', 'aki', '高千穂 亜樹'),
        10: ('Akashi Tatsuma', 'ttm', '明石 達真'),
        11: ('Yanagawa Sui', 'sui', '柳川 彗'),
        12: ('Ayasaki Komugi', 'kmg', '綾崎 小麦'),
        13: ('Orikasa Riku', 'rik', '折笠 凛久'),
        14: ('Munakata Touya', 'tuy', '宗像 十夜'),
        15: ('Usui Chihiro', 'chr', '碓井 千紘'),
        16: ('Kousaka Ango', 'ang', '香坂 安吾'),
        17: ('Kamijo Uta', 'uta', '上條 雅楽'),
        18: ('Shimizu Genshin', 'gns', '清水 弦心'),
    }

    def __init__(self, card_dict: dict):
        self.__card_data = card_dict

    def __str__(self):
        return dedent(
            f'''
            {self.name} {self.character_jp} ({self.character}) {self.rarity}\u2605
            {self.text}
            '''
        )

    @property
    def group(self) -> int:
        return self.card_id % 10_000

    @property
    def files(self, prefix=config.file_prefix, size='l') -> list:
        '''
        file name should be like this, img_card_chara_l_aki_0016_1.png
        but you can add a prefix just in case.
        i=0 -> unbloomed; i=1 -> bloomed
        '''
        return [f'{prefix}img_card_chara_{size}_{self.character_short}_{self.group:04d}_{i}.png' for i in range(2)]

    @property
    def character_jp(self):
        return self._character_list[self.__card_data.get('group_id')][2]

    @property
    def character_short(self) -> str:
        return self._character_list[self.__card_data.get('group_id')][1]

    @property
    def character(self) -> str:
        return self._character_list[self.__card_data.get('group_id')][0]

    @property
    def card_id(self) -> int:
        return self.__card_data.get('id')

    @property
    def rarity(self) -> int:
        return self.__card_data.get('rarity')

    @property
    def name(self) -> str:
        return self.__card_data.get('name')

    @property
    def text(self) -> str:
        return self.__card_data.get('text')


class DataNotFoundError(Exception):
    pass


def get_card_details(card_id: int) -> Card:
    global CARDS
    data = None
    for card in CARDS:
        if card.get('id') == card_id:
            data = card
    if not data:
        raise DataNotFoundError(f'{card_id} not found in CardData.json')
    return Card(data)


def send_card(api: tweepy.API, card: Card):
    # sanity check: gdrive mount might had failed
    if not border_files.exists():
        raise FileNotFoundError

    image_files = []
    for image_name in card.files:
        # this should return one file
        for image_path in config.illustration_path.glob(f'**/{image_name}'):
            image_files.append(image_path.open(mode='rb'))
    assert len(image_files) == 2, f'Too many images found? {card}'

    medias = [api.media_upload(fn, file=img).media_id_string
              for fn, img in zip(card.files, image_files)]
    api.update_status(status=f'{card}', media_ids=medias)


def random_card(recent=[], chara=None, extra=None) -> int:
    cid = 0
    while cid in recent or cid == 0:
        if chara is None:
            chara = randint(1, 18)
        if extra is None:
            rarity, group = choice(appearance[chara])
        else:
            rarity, group = choice(appearance[chara]+extra)
        cid = chara * 100_000 + rarity * 10_000 + group
    return cid


def main(api: tweepy.API) -> int:
    global CARDS
    with open('CardData.json', encoding='utf-8') as fj:
        CARDS = json.load(fj).get('Card')
    first_run = True
    run_data = config.illustration_path / 'data.bin'
    has_celebrate = {
        (28, 2): False,
        (21, 3): False,
        (9, 4): False,
        (13, 5): False,
        (28, 5): False,
        (24, 6): False,
    }
    recent = []
    done = set()
    if run_data.exists():
        with run_data.open(mode='rb') as spf:
            recent, done, has_celebrate = pickle.load(spf)
    try:
        while True:
            recent = recent[-10:]
            if not first_run:
                time.sleep(randint(25, 40) * 60)

            ctime = datetime.now(timezone(timedelta(hours=9)))
            day_month = (ctime.day, ctime.month)
            is_bday = day_month in bday_list.keys()

            if ctime.hour not in (0, 7, 9, 11, 13, 15, 17, 18, 19, 20, 21, 22, 23, 24):
                continue
            elif is_bday and not has_celebrate[day_month]:
                cid, *_ = bday_list[day_month]
                card = get_card_details(cid)
            elif is_bday and has_celebrate[day_month]:
                # bday card rarity == 5, group == 20
                cid = random_card(recent, bday_list[day_month][2], [(5, 20)])
                card = get_card_details(cid)
            elif config.photo_queue:
                cid = config.photo_queue.popleft()
                card = get_card_details(cid)
            else:
                cid = random_card(recent)
                card = get_card_details(cid)

            try:
                send_card(api, card)
            except tweepy.TweepError as twe:
                config.report(twe)
                return 1
            except FileNotFoundError as fnfe:
                config.report(fnfe)
                return 2
            except KeyboardInterrupt:
                config.report('Bot stopped by Keyboard interrupt')
                return 0
            except AssertionError as ae:
                config.report(ae)
                return 4
            else:
                recent.append(cid)
                done.add(cid)
                if first_run:
                    first_run = False
                if bday_list.get(day_month) is not None:
                    bday_card = bday_list.get(day_month)[0]
                    if cid == bday_card and not has_celebrate.get(day_month):
                        has_celebrate[day_month] = True
            finally:
                with run_data.open(mode='wb') as fo:
                    pickle.dump([recent, done, has_celebrate], fo)
    except KeyboardInterrupt:
        config.report('Bot stopped by Keyboard interrupt')
        return 0
    except DataNotFoundError as dnfe:
        config.report(dnfe)
        return 3


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(config.API_KEY, config.API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
    except:
        config.report("Error during authentication...")
    else:
        config.report("Authentication OK!")
        exit_code = main(api)
        sys.exit(exit_code)

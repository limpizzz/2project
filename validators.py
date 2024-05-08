import math
from db import execute_query
MAX_USER_STT_BLOCKS = 12  # выделяем на каждого пользователя по 12 аудиоблоков

# проверяем не превысил ли пользователь лимиты на преобразование аудио в текст
def is_stt_block_limit(user_id, duration):
    stt_blocks_num = math.ceil(duration / 15)

    sql_query = (
        f'SELECT SUM(stt_blocks) '
        f'FROM users_data '
        f'WHERE user_id = {user_id};')

    all_blocks = execute_query(sql_query) + stt_blocks_num

    if duration >= 30:
        return None, 'ошибка: аудио слишком длинное'

    if all_blocks > MAX_USER_STT_BLOCKS:
        return None, 'ошибка: лимит блоков превышен'
    else:
        return stt_blocks_num, 'все ок'


is_stt_block_limit(123, 31)